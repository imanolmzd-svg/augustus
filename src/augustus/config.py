"""Configuration and defaults for Augustus.

This module centralizes all configuration values and environment variables.
"""

import os
from pathlib import Path
from typing import List

# Version
VERSION = "0.1.0"

# Paths
DEFAULT_INDEX_DIR = Path.home() / ".augustus_index"
DEFAULT_CONFIG_DIR = Path.home() / ".augustus"

# Embedding configuration
DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
DEFAULT_EMBEDDING_PROVIDER = "openai"

# Chunking configuration
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

# Retrieval configuration
DEFAULT_TOP_K = 5
DEFAULT_SIMILARITY_THRESHOLD = 0.7

# Ignore patterns (similar to .gitignore)
DEFAULT_IGNORE_PATTERNS: List[str] = [
    # Version control
    ".git/",
    ".gitignore",
    ".gitattributes",
    # Dependencies
    "node_modules/",
    "venv/",
    "env/",
    ".venv/",
    "__pycache__/",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".Python",
    # Build artifacts
    "dist/",
    "build/",
    "*.egg-info/",
    "target/",
    "*.o",
    "*.so",
    "*.dylib",
    "*.dll",
    # IDE
    ".vscode/",
    ".idea/",
    "*.swp",
    "*.swo",
    ".DS_Store",
    # Binary files
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.ico",
    "*.pdf",
    "*.zip",
    "*.tar",
    "*.gz",
    "*.mp4",
    "*.mp3",
    # Secrets
    ".env",
    ".env.local",
    "*.key",
    "*.pem",
    "credentials.json",
    # Augustus-specific
    ".augustus/",
    ".augustus_index/",
]

# File size limits
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Output formatting
OUTPUT_WIDTH = 80
CITATION_FORMAT = "[{file}:{line}]"

# Environment variable overrides
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
INDEX_DIR = Path(os.getenv("AUGUSTUS_INDEX_DIR", str(DEFAULT_INDEX_DIR)))
