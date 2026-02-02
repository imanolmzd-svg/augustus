"""Tests for the vector index module."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from augustus.ingest.index import (
    VectorIndex,
    IngestSummary,
    ingest_dry_run,
    INDEX_DIR_NAME,
)
from augustus.ingest.splitter import DocumentChunk


class TestVectorIndex:
    """Tests for VectorIndex class."""

    def test_init_sets_paths(self, tmp_path):
        """VectorIndex should set correct paths."""
        index = VectorIndex(tmp_path)

        assert index.folder_path == tmp_path
        assert index.index_dir == tmp_path / INDEX_DIR_NAME
        assert index._vectorstore is None

    def test_exists_returns_false_when_no_index(self, tmp_path):
        """exists() should return False when no index exists."""
        index = VectorIndex(tmp_path)
        assert index.exists() is False

    def test_exists_returns_true_when_index_files_exist(self, tmp_path):
        """exists() should return True when index files exist."""
        index_dir = tmp_path / INDEX_DIR_NAME
        index_dir.mkdir()
        (index_dir / "index.faiss").touch()
        (index_dir / "index.pkl").touch()

        index = VectorIndex(tmp_path)
        assert index.exists() is True

    def test_build_raises_on_empty_chunks(self, tmp_path):
        """build() should raise ValueError on empty chunks."""
        index = VectorIndex(tmp_path)

        with pytest.raises(ValueError, match="No chunks to index"):
            index.build([])

    def test_build_raises_without_api_key(self, tmp_path, monkeypatch):
        """build() should raise ValueError without API key."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        index = VectorIndex(tmp_path)
        chunks = [
            DocumentChunk(
                id="test_0",
                content="Test content",
                source_path="test.txt",
                chunk_index=0,
                metadata={},
            )
        ]

        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            index.build(chunks)

    def test_save_raises_without_build(self, tmp_path):
        """save() should raise ValueError if build() not called."""
        index = VectorIndex(tmp_path)

        with pytest.raises(ValueError, match="No index to save"):
            index.save()

    def test_load_returns_false_when_no_index(self, tmp_path, monkeypatch):
        """load() should return False when no index exists."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        index = VectorIndex(tmp_path)
        assert index.load() is False

    def test_search_returns_empty_when_no_index(self, tmp_path):
        """search() should return empty list when no index."""
        index = VectorIndex(tmp_path)
        results = index.search("test query")
        assert results == []


class TestIngestDryRun:
    """Tests for ingest_dry_run function."""

    def test_returns_summary(self, tmp_path):
        """ingest_dry_run should return IngestSummary."""
        # Create some test files
        (tmp_path / "test.txt").write_text("Hello world")
        (tmp_path / "other.py").write_text("print('hello')")

        summary = ingest_dry_run(tmp_path)

        assert isinstance(summary, IngestSummary)
        assert summary.loaded == 2
        assert summary.chunks == 0  # dry-run doesn't chunk
        assert len(summary.sample_paths) <= 5

    def test_respects_sample_size(self, tmp_path):
        """ingest_dry_run should respect sample_size parameter."""
        for i in range(10):
            (tmp_path / f"file{i}.txt").write_text(f"Content {i}")

        summary = ingest_dry_run(tmp_path, sample_size=3)

        assert len(summary.sample_paths) == 3

    def test_empty_folder(self, tmp_path):
        """ingest_dry_run should handle empty folders."""
        summary = ingest_dry_run(tmp_path)

        assert summary.loaded == 0
        assert summary.sample_paths == []


class TestIngestSummary:
    """Tests for IngestSummary dataclass."""

    def test_is_frozen(self):
        """IngestSummary should be immutable."""
        summary = IngestSummary(
            discovered=10,
            ignored=2,
            loaded=8,
            chunks=24,
            sample_paths=["a.txt"],
        )

        with pytest.raises(AttributeError):
            summary.loaded = 100
