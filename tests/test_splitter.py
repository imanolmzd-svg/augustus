"""Tests for the document splitter module."""

import pytest

from augustus.ingest.loader import LoadedDocument
from augustus.ingest.splitter import (
    DocumentChunk,
    create_splitter,
    split_document,
    split_documents,
    split_text,
)


class TestSplitText:
    """Tests for split_text function."""

    def test_short_text_no_split(self):
        """Short text should not be split."""
        text = "Hello world"
        chunks = split_text(text, chunk_size=100, chunk_overlap=20)
        assert len(chunks) == 1
        assert chunks[0] == text

    def test_long_text_splits(self):
        """Long text should be split into multiple chunks."""
        text = "word " * 500  # ~2500 chars
        chunks = split_text(text, chunk_size=500, chunk_overlap=50)
        assert len(chunks) > 1

    def test_chunk_overlap(self):
        """Chunks should have overlapping content."""
        text = "A" * 300 + " " + "B" * 300 + " " + "C" * 300
        chunks = split_text(text, chunk_size=400, chunk_overlap=100)

        # With overlap, adjacent chunks should share some content
        assert len(chunks) >= 2

    def test_empty_text(self):
        """Empty text should return empty list."""
        chunks = split_text("", chunk_size=100, chunk_overlap=20)
        assert chunks == []


class TestCreateSplitter:
    """Tests for create_splitter function."""

    def test_default_parameters(self):
        """Splitter should use default parameters."""
        splitter = create_splitter()
        assert splitter._chunk_size == 1000
        assert splitter._chunk_overlap == 200

    def test_custom_parameters(self):
        """Splitter should accept custom parameters."""
        splitter = create_splitter(chunk_size=500, chunk_overlap=50)
        assert splitter._chunk_size == 500
        assert splitter._chunk_overlap == 50


class TestSplitDocument:
    """Tests for split_document function."""

    def test_single_chunk_document(self):
        """Small document should produce single chunk."""
        doc = LoadedDocument(
            id="test123",
            relative_path="test.txt",
            content="Short content",
            metadata={"size_bytes": 13},
        )

        chunks = split_document(doc, chunk_size=1000, chunk_overlap=100)

        assert len(chunks) == 1
        assert isinstance(chunks[0], DocumentChunk)
        assert chunks[0].content == "Short content"
        assert chunks[0].source_path == "test.txt"
        assert chunks[0].chunk_index == 0
        assert chunks[0].id == "test123_0"

    def test_multi_chunk_document(self):
        """Large document should produce multiple chunks."""
        doc = LoadedDocument(
            id="test456",
            relative_path="big.txt",
            content="word " * 500,
            metadata={"size_bytes": 2500},
        )

        chunks = split_document(doc, chunk_size=500, chunk_overlap=50)

        assert len(chunks) > 1
        for i, chunk in enumerate(chunks):
            assert chunk.source_path == "big.txt"
            assert chunk.chunk_index == i
            assert chunk.id == f"test456_{i}"
            assert chunk.metadata["total_chunks"] == len(chunks)

    def test_metadata_preserved(self):
        """Original metadata should be preserved in chunks."""
        doc = LoadedDocument(
            id="test789",
            relative_path="meta.txt",
            content="Some content",
            metadata={"size_bytes": 12, "extension": ".txt"},
        )

        chunks = split_document(doc)

        assert chunks[0].metadata["size_bytes"] == 12
        assert chunks[0].metadata["extension"] == ".txt"
        assert chunks[0].metadata["source"] == "meta.txt"


class TestSplitDocuments:
    """Tests for split_documents function."""

    def test_multiple_documents(self):
        """Multiple documents should all be chunked."""
        docs = [
            LoadedDocument(
                id="doc1",
                relative_path="a.txt",
                content="Content A",
                metadata={},
            ),
            LoadedDocument(
                id="doc2",
                relative_path="b.txt",
                content="Content B",
                metadata={},
            ),
        ]

        chunks = split_documents(docs)

        assert len(chunks) == 2
        paths = {c.source_path for c in chunks}
        assert paths == {"a.txt", "b.txt"}

    def test_empty_list(self):
        """Empty document list should return empty chunk list."""
        chunks = split_documents([])
        assert chunks == []
