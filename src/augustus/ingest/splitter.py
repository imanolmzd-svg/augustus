"""Text chunking logic for Augustus.

This module handles splitting documents into chunks for embedding.
Uses LangChain text splitters for consistent, deterministic chunking.
"""

from dataclasses import dataclass
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from augustus.config import DEFAULT_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE
from augustus.ingest.loader import LoadedDocument


@dataclass(frozen=True)
class DocumentChunk:
    """A chunk of a document ready for embedding."""

    id: str
    content: str
    source_path: str
    chunk_index: int
    metadata: dict


def create_splitter(
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> RecursiveCharacterTextSplitter:
    """Create a text splitter with the given parameters.

    Args:
        chunk_size: Target size for each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks

    Returns:
        Configured RecursiveCharacterTextSplitter
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", " ", ""],
    )


def split_document(
    document: LoadedDocument,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[DocumentChunk]:
    """Split a single document into chunks.

    Args:
        document: The loaded document to split
        chunk_size: Target size for each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks

    Returns:
        List of DocumentChunk objects
    """
    splitter = create_splitter(chunk_size, chunk_overlap)
    text_chunks = splitter.split_text(document.content)

    chunks = []
    for i, text in enumerate(text_chunks):
        chunk_id = f"{document.id}_{i}"
        chunks.append(
            DocumentChunk(
                id=chunk_id,
                content=text,
                source_path=document.relative_path,
                chunk_index=i,
                metadata={
                    **document.metadata,
                    "source": document.relative_path,
                    "chunk_index": i,
                    "total_chunks": len(text_chunks),
                },
            )
        )

    return chunks


def split_documents(
    documents: List[LoadedDocument],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[DocumentChunk]:
    """Split multiple documents into chunks.

    Args:
        documents: List of loaded documents
        chunk_size: Target size for each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks

    Returns:
        List of DocumentChunk objects from all documents
    """
    all_chunks = []
    for doc in documents:
        chunks = split_document(doc, chunk_size, chunk_overlap)
        all_chunks.extend(chunks)

    return all_chunks


def split_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[str]:
    """Split a single text into chunks.

    Args:
        text: Text to split
        chunk_size: Target size for each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    splitter = create_splitter(chunk_size, chunk_overlap)
    return splitter.split_text(text)
