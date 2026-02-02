"""Vector index building for Augustus.

This module handles creating and managing the FAISS vector index
for semantic search over document chunks.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from augustus.ingest.loader import LoadedDocument, load_folder
from augustus.ingest.splitter import DocumentChunk, split_documents

# Index directory name (stored inside the indexed folder)
INDEX_DIR_NAME = ".augustus"
INDEX_FILE_NAME = "index.faiss"
DOCSTORE_FILE_NAME = "docstore.json"


@dataclass(frozen=True)
class IngestSummary:
    """Summary of an ingestion run."""

    discovered: int
    ignored: int
    loaded: int
    chunks: int
    sample_paths: List[str]


class VectorIndex:
    """Local vector index for semantic search using FAISS.

    The index is stored in .augustus/ inside the indexed folder.
    """

    def __init__(self, folder_path: Path):
        """Initialize the vector index.

        Args:
            folder_path: Path to the folder being indexed
        """
        self.folder_path = folder_path.resolve()
        self.index_dir = self.folder_path / INDEX_DIR_NAME
        self.index_path = self.index_dir / INDEX_FILE_NAME
        self._vectorstore = None

    def build(
        self,
        chunks: List[DocumentChunk],
        embedding_model: str = "text-embedding-3-small",
    ) -> int:
        """Build the vector index from chunks.

        Args:
            chunks: List of DocumentChunk objects to index
            embedding_model: OpenAI embedding model to use

        Returns:
            Number of chunks indexed

        Raises:
            ValueError: If no chunks provided or API key missing
        """
        if not chunks:
            raise ValueError("No chunks to index")

        import os

        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY environment variable not set. "
                "Set it with: export OPENAI_API_KEY=your-key"
            )

        from langchain_community.vectorstores import FAISS
        from langchain_openai import OpenAIEmbeddings

        # Prepare texts and metadatas for FAISS
        texts = [chunk.content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        # Create embeddings and build index
        embeddings = OpenAIEmbeddings(model=embedding_model)
        self._vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas,
        )

        return len(chunks)

    def save(self) -> Path:
        """Save the index to disk.

        Returns:
            Path to the saved index directory

        Raises:
            ValueError: If no index has been built
        """
        if self._vectorstore is None:
            raise ValueError("No index to save. Call build() first.")

        # Create index directory
        self.index_dir.mkdir(parents=True, exist_ok=True)

        # Save FAISS index
        self._vectorstore.save_local(str(self.index_dir))

        return self.index_dir

    def load(self) -> bool:
        """Load the index from disk.

        Returns:
            True if index loaded successfully, False otherwise
        """
        if not self.exists():
            return False

        import os

        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY environment variable not set. "
                "Set it with: export OPENAI_API_KEY=your-key"
            )

        from langchain_community.vectorstores import FAISS
        from langchain_openai import OpenAIEmbeddings

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self._vectorstore = FAISS.load_local(
            str(self.index_dir),
            embeddings,
            allow_dangerous_deserialization=True,
        )
        return True

    def exists(self) -> bool:
        """Check if an index exists at the configured path.

        Returns:
            True if index exists, False otherwise
        """
        # FAISS saves as index.faiss and index.pkl
        faiss_file = self.index_dir / "index.faiss"
        pkl_file = self.index_dir / "index.pkl"
        return faiss_file.exists() and pkl_file.exists()

    def search(self, query: str, k: int = 5) -> List[dict]:
        """Search the index for similar documents.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of results with content, metadata, and score
        """
        if self._vectorstore is None:
            if not self.load():
                return []

        results = self._vectorstore.similarity_search_with_score(query, k=k)

        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score),
            }
            for doc, score in results
        ]


def ingest_folder(
    folder_path: Path,
    ignore_patterns: Optional[List[str]] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    embedding_model: str = "text-embedding-3-small",
) -> IngestSummary:
    """Ingest a folder: load files, chunk, embed, and save index.

    Args:
        folder_path: Path to folder to ingest
        ignore_patterns: Additional patterns to ignore
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
        embedding_model: OpenAI embedding model to use

    Returns:
        IngestSummary with statistics
    """
    # Load documents
    loaded, discovered, ignored = load_folder(folder_path, ignore_patterns)

    if not loaded:
        return IngestSummary(
            discovered=discovered,
            ignored=ignored,
            loaded=0,
            chunks=0,
            sample_paths=[],
        )

    # Split into chunks
    chunks = split_documents(loaded, chunk_size, chunk_overlap)

    # Build and save index
    index = VectorIndex(folder_path)
    index.build(chunks, embedding_model)
    index.save()

    sample_paths = [doc.relative_path for doc in loaded][:5]

    return IngestSummary(
        discovered=discovered,
        ignored=ignored,
        loaded=len(loaded),
        chunks=len(chunks),
        sample_paths=sample_paths,
    )


def ingest_dry_run(
    folder_path: Path,
    sample_size: int = 5,
    ignore_patterns: Optional[List[str]] = None,
) -> IngestSummary:
    """Run ingestion in dry-run mode (no embedding, no index).

    Args:
        folder_path: Path to folder to analyze
        sample_size: Number of sample paths to return
        ignore_patterns: Additional patterns to ignore

    Returns:
        IngestSummary with statistics (chunks=0 in dry-run)
    """
    loaded, discovered, ignored = load_folder(folder_path, ignore_patterns)
    sample_paths = [doc.relative_path for doc in loaded][:sample_size]

    return IngestSummary(
        discovered=discovered,
        ignored=ignored,
        loaded=len(loaded),
        chunks=0,
        sample_paths=sample_paths,
    )
