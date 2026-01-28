"""Vector index building for Augustus."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from augustus.ingest.loader import LoadedDocument, load_folder


class VectorIndex:
    """Local vector index for semantic search.
    
    This is a placeholder class. Future implementation will use FAISS or Chroma.
    """
    
    def __init__(self, index_path: Optional[Path] = None):
        """Initialize the vector index.
        
        Args:
            index_path: Path to store the index (if None, use default)
        """
        self.index_path = index_path
        self._index = None
    
    def build(self, chunks: List[dict]) -> None:
        """Build the vector index from chunks.
        
        Args:
            chunks: List of chunk dictionaries with content and metadata
            
        Note:
            This is a placeholder. Future implementation will embed and index chunks.
        """
        pass
    
    def save(self) -> None:
        """Save the index to disk.
        
        Note:
            This is a placeholder. Future implementation will persist the index.
        """
        pass
    
    def load(self) -> None:
        """Load the index from disk.
        
        Note:
            This is a placeholder. Future implementation will load persisted index.
        """
        pass
    
    def exists(self) -> bool:
        """Check if an index exists at the configured path.
        
        Returns:
            True if index exists, False otherwise
        """
        return False


@dataclass(frozen=True)
class IngestSummary:
    """Summary of an ingestion run."""

    discovered: int
    ignored: int
    loaded: int
    sample_paths: List[str]


def ingest_folder(
    folder_path: Path,
    ignore_patterns: Optional[List[str]] = None,
) -> List[LoadedDocument]:
    """Ingest a folder and return loaded documents."""
    loaded, _, _ = load_folder(folder_path, ignore_patterns=ignore_patterns)
    return loaded


def ingest_dry_run(
    folder_path: Path,
    sample_size: int = 5,
    ignore_patterns: Optional[List[str]] = None,
) -> IngestSummary:
    """Run ingestion and return counts plus a sample path list."""
    loaded, discovered, ignored = load_folder(folder_path, ignore_patterns=ignore_patterns)
    sample_paths = [doc.relative_path for doc in loaded][:sample_size]
    return IngestSummary(
        discovered=discovered,
        ignored=ignored,
        loaded=len(loaded),
        sample_paths=sample_paths,
    )
