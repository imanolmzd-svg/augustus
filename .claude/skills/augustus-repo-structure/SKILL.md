---
name: augustus-repo-structure
description: Enforce the repository structure and architectural boundaries of Augustus. Apply when creating files, refactoring code, adding modules, or discussing architecture.
---

# Repository Structure Rules

## High-level layout
The project follows a **simple, explicit, layered structure**.

Expected layout:
src/augustus/
cli.py
ingest/
qa/
utils/
config.py
docs/
tests/
examples/


## Folder responsibilities

### `cli.py`
- CLI entrypoint
- Argument parsing
- User-facing output
- No business logic

### `ingest/`
- Folder traversal
- File loading
- Ignore rules
- Chunking
- Embeddings
- Index building

### `qa/`
- Retrieval logic
- Prompt construction
- Answer generation
- Citation formatting

### `utils/`
- Shared helpers
- File tree generation
- Hashing, filtering, formatting
- No LangChain-specific logic

### `config.py`
- Defaults
- Environment variables
- Centralized configuration

## Architectural Rules
- CLI never talks directly to vector stores
- Ingest and QA are decoupled
- Utilities must not depend on LangChain
- No circular imports

## Naming & Style
- Explicit over clever
- Clear function names
- Small files, single responsibility
- Prefer adding a new file over growing a “god file”

When in doubt: choose clarity over abstraction.