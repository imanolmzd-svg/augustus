"""File tree generation utilities for Augustus.

This module generates readable file tree representations.
No LangChain dependencies - pure Python only.
"""

from pathlib import Path
from typing import List, Optional, Set


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
