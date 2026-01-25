# Architecture

Augustus follows a simple, layered architecture with clear separation of concerns.

## High-Level Structure

```
src/augustus/
├── cli.py          # CLI entrypoint (Typer)
├── config.py       # Configuration and defaults
├── ingest/         # Folder loading, chunking, indexing
├── qa/             # Retrieval and answer generation
└── utils/          # Shared helpers (no LangChain)
```

## Module Responsibilities

### CLI (`cli.py`)
- Argument parsing with Typer
- User-facing output
- No business logic

### Ingest (`ingest/`)
- `loader.py` - File loading with LangChain document loaders
- `splitter.py` - Text chunking with LangChain text splitters
- `index.py` - Vector index building with FAISS

### QA (`qa/`)
- `retriever.py` - Semantic search and document retrieval
- `prompt.py` - Prompt template construction
- `answer.py` - Answer generation and citation formatting

### Utils (`utils/`)
- `file_tree.py` - File tree generation
- `ignore.py` - Gitignore-style pattern matching
- `formatting.py` - Output formatting helpers
- Pure Python, no LangChain dependencies

### Config (`config.py`)
- Default values
- Environment variable handling
- Centralized configuration

## Design Principles

1. **Separation of concerns** - Each module has a single responsibility
2. **No circular imports** - Clean dependency graph
3. **CLI is thin** - Business logic lives in modules
4. **Utils are pure** - No framework dependencies in utilities
5. **Evidence-first** - All answers must be grounded in indexed files

## Data Flow

1. **Indexing**: folder → loader → splitter → embeddings → vector index
2. **Querying**: question → retriever → context → prompt → LLM → answer + citations

## Future Enhancements

This document will be updated as the implementation progresses.
