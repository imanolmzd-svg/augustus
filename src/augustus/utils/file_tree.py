"""File tree generation utilities for Augustus.

This module generates readable file tree representations.
No LangChain dependencies - pure Python only.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from augustus.utils.ignore import IgnoreSpec, build_ignore_spec, should_ignore


@dataclass(frozen=True)
class FileRecord:
    """Normalized file record for ingestion."""

    absolute_path: Path
    relative_path: str
    size_bytes: int
    extension: str


def generate_tree(
    root_path: Path,
    ignore_patterns: Optional[List[str]] = None,
    max_depth: Optional[int] = None,
) -> str:
    """Generate a text-based file tree representation.
    
    Args:
        root_path: Root directory path
        ignore_patterns: List of patterns to ignore (gitignore-style)
        max_depth: Maximum depth to traverse (None for unlimited)
        
    Returns:
        String representation of the file tree
    """
    if not root_path.exists():
        return f"Path does not exist: {root_path}"
    
    if not root_path.is_dir():
        return f"Not a directory: {root_path}"
    
    lines = [str(root_path.name) + "/"]
    _build_tree(root_path, "", lines, ignore_patterns or [], max_depth, 0)
    return "\n".join(lines)


def _build_tree(
    path: Path,
    prefix: str,
    lines: List[str],
    ignore_patterns: List[str],
    max_depth: Optional[int],
    current_depth: int,
) -> None:
    """Recursively build the tree structure.
    
    Args:
        path: Current directory path
        prefix: Prefix for tree formatting
        lines: List to accumulate output lines
        ignore_patterns: Patterns to ignore
        max_depth: Maximum depth
        current_depth: Current recursion depth
    """
    if max_depth is not None and current_depth >= max_depth:
        return
    
    try:
        entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name))
    except PermissionError:
        return
    
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        
        # Skip ignored patterns (simplified check)
        if _should_ignore(entry, ignore_patterns):
            continue
        
        # Format tree branch
        connector = "└── " if is_last else "├── "
        name = entry.name + ("/" if entry.is_dir() else "")
        lines.append(f"{prefix}{connector}{name}")
        
        # Recurse into directories
        if entry.is_dir():
            extension = "    " if is_last else "│   "
            _build_tree(
                entry,
                prefix + extension,
                lines,
                ignore_patterns,
                max_depth,
                current_depth + 1,
            )


def _should_ignore(path: Path, ignore_patterns: List[str]) -> bool:
    """Check if a path should be ignored based on patterns.
    
    Args:
        path: Path to check
        ignore_patterns: List of patterns
        
    Returns:
        True if path should be ignored
        
    Note:
        This is a simplified implementation. Future version may use gitignore-style matching.
    """
    name = path.name
    
    # Check exact matches and simple patterns
    for pattern in ignore_patterns:
        pattern = pattern.rstrip("/")
        
        # Exact match
        if name == pattern:
            return True
        
        # Directory match
        if pattern.endswith("/") and path.is_dir() and name == pattern[:-1]:
            return True
        
        # Wildcard patterns (simplified)
        if "*" in pattern:
            import fnmatch
            if fnmatch.fnmatch(name, pattern):
                return True
    
    return False


def collect_files(
    root_path: Path,
    ignore_spec: Optional[IgnoreSpec] = None,
    extra_ignore_patterns: Optional[List[str]] = None,
) -> Tuple[List[FileRecord], int]:
    """Collect file records under a root path.

    Args:
        root_path: Root directory path
        ignore_spec: Optional ignore spec to reuse
        extra_ignore_patterns: Additional ignore patterns to apply

    Returns:
        Tuple of (file_records, ignored_count)
    """
    if not root_path.exists() or not root_path.is_dir():
        return [], 0

    if ignore_spec is None:
        ignore_spec = build_ignore_spec(root_path, extra_ignore_patterns)

    records: List[FileRecord] = []
    ignored_count = 0
    stack = [root_path]

    while stack:
        current = stack.pop()
        try:
            entries = sorted(current.iterdir(), key=lambda p: p.name)
        except PermissionError:
            ignored_count += 1
            continue

        dirs: List[Path] = []
        for entry in entries:
            if should_ignore(entry, base_path=root_path, ignore_spec=ignore_spec):
                ignored_count += 1
                continue

            if entry.is_dir():
                dirs.append(entry)
                continue

            if not entry.is_file():
                continue

            try:
                size_bytes = entry.stat().st_size
            except OSError:
                ignored_count += 1
                continue

            try:
                rel_path = entry.relative_to(root_path).as_posix()
            except ValueError:
                rel_path = entry.name

            records.append(
                FileRecord(
                    absolute_path=entry.resolve(),
                    relative_path=rel_path,
                    size_bytes=size_bytes,
                    extension=entry.suffix.lower(),
                )
            )

        for directory in reversed(dirs):
            stack.append(directory)

    records.sort(key=lambda record: record.relative_path)
    return records, ignored_count


def list_files(
    root_path: Path,
    ignore_spec: Optional[IgnoreSpec] = None,
    extra_ignore_patterns: Optional[List[str]] = None,
) -> List[FileRecord]:
    """Return a normalized, deterministic list of file records."""
    records, _ = collect_files(
        root_path,
        ignore_spec=ignore_spec,
        extra_ignore_patterns=extra_ignore_patterns,
    )
    return records


def count_files(
    root_path: Path,
    ignore_patterns: Optional[List[str]] = None,
) -> tuple[int, int]:
    """Count files and directories in a tree.
    
    Args:
        root_path: Root directory path
        ignore_patterns: List of patterns to ignore
        
    Returns:
        Tuple of (file_count, directory_count)
    """
    if not root_path.exists() or not root_path.is_dir():
        return 0, 0
    
    file_count = 0
    dir_count = 0
    ignore_patterns = ignore_patterns or []
    
    try:
        for entry in root_path.rglob("*"):
            if _should_ignore(entry, ignore_patterns):
                continue
            
            if entry.is_file():
                file_count += 1
            elif entry.is_dir():
                dir_count += 1
    except PermissionError:
        pass
    
    return file_count, dir_count
