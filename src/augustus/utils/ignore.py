"""Ignore pattern handling for Augustus.

This module handles gitignore-style pattern matching.
No LangChain dependencies - pure Python only.
"""

import fnmatch
from pathlib import Path
from typing import List, Optional

from augustus.config import DEFAULT_IGNORE_PATTERNS


class IgnoreSpec:
    """Handles gitignore-style ignore patterns.
    
    This is a simplified implementation. Future versions may use
    a library like pathspec for full gitignore compatibility.
    """
    
    def __init__(self, patterns: Optional[List[str]] = None):
        """Initialize ignore spec with patterns.
        
        Args:
            patterns: List of gitignore-style patterns
        """
        self.patterns = patterns or []
    
    def should_ignore(self, path: Path, base_path: Optional[Path] = None) -> bool:
        """Check if a path should be ignored.
        
        Args:
            path: Path to check
            base_path: Base path for relative matching
            
        Returns:
            True if path matches any ignore pattern
        """
        if not self.patterns:
            return False
        
        # Get relative path if base_path provided
        if base_path:
            try:
                rel_path = path.relative_to(base_path)
            except ValueError:
                rel_path = path
        else:
            rel_path = path
        
        path_str = str(rel_path)
        name = path.name
        
        for pattern in self.patterns:
            if self._matches_pattern(name, path_str, pattern, path.is_dir()):
                return True
        
        return False
    
    def _matches_pattern(
        self,
        name: str,
        path_str: str,
        pattern: str,
        is_dir: bool,
    ) -> bool:
        """Check if a path matches a specific pattern.
        
        Args:
            name: File/directory name
            path_str: Full path string
            pattern: Pattern to match against
            is_dir: Whether path is a directory
            
        Returns:
            True if pattern matches
        """
        # Remove leading/trailing slashes
        pattern = pattern.strip()
        
        # Skip empty patterns
        if not pattern:
            return False
        
        # Directory-specific patterns
        if pattern.endswith("/"):
            if not is_dir:
                return False
            pattern = pattern[:-1]
        
        # Exact name match
        if pattern == name:
            return True
        
        # Wildcard matching
        if "*" in pattern or "?" in pattern:
            # Simple wildcard on name
            if "/" not in pattern:
                return fnmatch.fnmatch(name, pattern)
            # Path-based wildcard
            return fnmatch.fnmatch(path_str, pattern)
        
        # Substring match for paths
        if "/" in pattern:
            return pattern in path_str
        
        return False
    
    def add_pattern(self, pattern: str) -> None:
        """Add a new ignore pattern.
        
        Args:
            pattern: Pattern to add
        """
        if pattern and pattern not in self.patterns:
            self.patterns.append(pattern)
    
    def remove_pattern(self, pattern: str) -> None:
        """Remove an ignore pattern.
        
        Args:
            pattern: Pattern to remove
        """
        if pattern in self.patterns:
            self.patterns.remove(pattern)


def load_gitignore(path: Path) -> List[str]:
    """Load patterns from a .gitignore file.
    
    Args:
        path: Path to .gitignore file
        
    Returns:
        List of patterns (excluding comments and empty lines)
    """
    if not path.exists() or not path.is_file():
        return []
    
    patterns = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith("#"):
                    patterns.append(line)
    except Exception:
        # If we can't read the file, return empty list
        pass
    
    return patterns


def merge_patterns(
    default_patterns: List[str],
    custom_patterns: Optional[List[str]] = None,
) -> List[str]:
    """Merge default and custom ignore patterns.
    
    Args:
        default_patterns: Default patterns
        custom_patterns: Additional custom patterns
        
    Returns:
        Combined list of unique patterns
    """
    merged = list(default_patterns)
    
    if custom_patterns:
        for pattern in custom_patterns:
            if pattern not in merged:
                merged.append(pattern)
    
    return merged


def build_ignore_spec(
    base_path: Optional[Path] = None,
    extra_patterns: Optional[List[str]] = None,
) -> IgnoreSpec:
    """Build an IgnoreSpec from defaults and optional .gitignore.

    Args:
        base_path: Base directory for .gitignore lookup
        extra_patterns: Additional patterns to include

    Returns:
        IgnoreSpec configured with merged patterns
    """
    patterns = merge_patterns(DEFAULT_IGNORE_PATTERNS, extra_patterns)

    if base_path is not None:
        gitignore_path = base_path / ".gitignore"
        gitignore_patterns = load_gitignore(gitignore_path)
        patterns = merge_patterns(patterns, gitignore_patterns)

    return IgnoreSpec(patterns)


def should_ignore(
    path: Path,
    base_path: Optional[Path] = None,
    ignore_spec: Optional[IgnoreSpec] = None,
    extra_patterns: Optional[List[str]] = None,
) -> bool:
    """Check if a path should be ignored.

    Args:
        path: Path to evaluate
        base_path: Base directory for relative matching
        ignore_spec: Optional IgnoreSpec to reuse
        extra_patterns: Additional patterns to include if ignore_spec not given

    Returns:
        True if the path should be ignored
    """
    if ignore_spec is None:
        ignore_spec = build_ignore_spec(base_path, extra_patterns)

    return ignore_spec.should_ignore(path, base_path=base_path)
