"""Output formatting utilities for Augustus.

This module provides helpers for formatting CLI output.
No LangChain dependencies - pure Python only.
"""

from typing import List, Optional


def format_header(text: str, width: int = 80) -> str:
    """Format a header with borders.
    
    Args:
        text: Header text
        width: Total width in characters
        
    Returns:
        Formatted header string
    """
    border = "=" * width
    padding = (width - len(text) - 2) // 2
    centered = f"{' ' * padding}{text}{' ' * padding}"
    
    # Adjust for odd widths
    if len(centered) < width - 2:
        centered += " "
    
    return f"{border}\n {centered} \n{border}"


def format_section(title: str, content: str, width: int = 80) -> str:
    """Format a section with title and content.
    
    Args:
        title: Section title
        content: Section content
        width: Total width in characters
        
    Returns:
        Formatted section string
    """
    separator = "-" * width
    return f"\n{title}\n{separator}\n{content}\n"


def format_list(
    items: List[str],
    numbered: bool = False,
    indent: int = 0,
) -> str:
    """Format a list of items.
    
    Args:
        items: List of items to format
        numbered: Use numbered list instead of bullets
        indent: Number of spaces to indent
        
    Returns:
        Formatted list string
    """
    if not items:
        return ""
    
    indent_str = " " * indent
    lines = []
    
    for i, item in enumerate(items, 1):
        if numbered:
            prefix = f"{i}. "
        else:
            prefix = "- "
        lines.append(f"{indent_str}{prefix}{item}")
    
    return "\n".join(lines)


def format_key_value(
    key: str,
    value: str,
    key_width: int = 20,
) -> str:
    """Format a key-value pair.
    
    Args:
        key: Key string
        value: Value string
        key_width: Width for key column
        
    Returns:
        Formatted key-value string
    """
    return f"{key:<{key_width}} {value}"


def format_table(
    headers: List[str],
    rows: List[List[str]],
    column_widths: Optional[List[int]] = None,
) -> str:
    """Format a simple text table.
    
    Args:
        headers: List of column headers
        rows: List of rows (each row is a list of values)
        column_widths: Optional list of column widths
        
    Returns:
        Formatted table string
    """
    if not headers or not rows:
        return ""
    
    # Calculate column widths if not provided
    if column_widths is None:
        column_widths = []
        for i, header in enumerate(headers):
            max_width = len(header)
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(row[i]))
            column_widths.append(max_width + 2)
    
    # Format header
    header_line = "".join(
        f"{h:<{w}}" for h, w in zip(headers, column_widths)
    )
    separator = "-" * sum(column_widths)
    
    # Format rows
    row_lines = []
    for row in rows:
        row_line = "".join(
            f"{v:<{w}}" for v, w in zip(row, column_widths)
        )
        row_lines.append(row_line)
    
    return f"{header_line}\n{separator}\n" + "\n".join(row_lines)


def wrap_text(text: str, width: int = 80, indent: int = 0) -> str:
    """Wrap text to a specific width.
    
    Args:
        text: Text to wrap
        width: Maximum line width
        indent: Number of spaces to indent wrapped lines
        
    Returns:
        Wrapped text string
    """
    import textwrap
    
    wrapper = textwrap.TextWrapper(
        width=width,
        subsequent_indent=" " * indent,
    )
    
    return wrapper.fill(text)


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
