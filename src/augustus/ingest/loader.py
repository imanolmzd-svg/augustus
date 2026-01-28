"""File loading logic for Augustus."""

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from augustus.config import MAX_FILE_SIZE_BYTES
from augustus.utils.file_tree import FileRecord, collect_files
from augustus.utils.ignore import build_ignore_spec


@dataclass(frozen=True)
class LoadedDocument:
    """A loaded file with metadata for ingestion."""

    id: str
    relative_path: str
    content: str
    metadata: Dict[str, object]


def _is_binary_bytes(raw: bytes) -> bool:
    if b"\x00" in raw:
        return True
    return False


def _stable_id(relative_path: str, content: str) -> str:
    payload = f"{relative_path}\n{content}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_file(
    file_path: Path,
    base_path: Optional[Path] = None,
    size_bytes: Optional[int] = None,
    extension: Optional[str] = None,
) -> Optional[LoadedDocument]:
    """Load a single file as text if possible."""
    try:
        if size_bytes is None:
            size_bytes = file_path.stat().st_size
    except OSError:
        return None

    if size_bytes > MAX_FILE_SIZE_BYTES:
        return None

    try:
        raw = file_path.read_bytes()
    except OSError:
        return None

    if _is_binary_bytes(raw):
        return None

    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None

    if base_path is not None:
        try:
            relative_path = file_path.relative_to(base_path).as_posix()
        except ValueError:
            relative_path = file_path.name
    else:
        relative_path = file_path.name

    doc_id = _stable_id(relative_path, content)
    metadata = {
        "size_bytes": size_bytes,
        "extension": extension if extension is not None else file_path.suffix.lower(),
    }

    return LoadedDocument(
        id=doc_id,
        relative_path=relative_path,
        content=content,
        metadata=metadata,
    )


def load_folder(
    folder_path: Path,
    ignore_patterns: Optional[List[str]] = None,
) -> Tuple[List[LoadedDocument], int, int]:
    """Load all text files from a folder.

    Returns:
        Tuple of (loaded_documents, discovered_count, ignored_count)
    """
    ignore_spec = build_ignore_spec(folder_path, ignore_patterns)
    records, ignored_count = collect_files(folder_path, ignore_spec=ignore_spec)

    loaded: List[LoadedDocument] = []
    for record in records:
        doc = load_file(
            record.absolute_path,
            base_path=folder_path,
            size_bytes=record.size_bytes,
            extension=record.extension,
        )
        if doc is None:
            ignored_count += 1
            continue
        loaded.append(doc)

    return loaded, len(records), ignored_count
