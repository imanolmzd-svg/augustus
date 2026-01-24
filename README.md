# Augustus

Augustus is a small, local-first CLI tool that helps you understand and query the contents of a folder. It indexes your files, builds a semantic search index locally, and answers questions using only the information found in those files.

## Why Augustus Exists

When exploring an unfamiliar codebase or folder structure, you often need to answer questions like: What does this project do? Where is the main logic? What technologies are used? Augustus answers these questions by treating the folder itself as the source of truth—no external data, no guessing.

## What Augustus Can Do

- Index a folder's structure and text files
- Build a local semantic index for retrieval
- Answer questions based on file contents
- Cite sources with file paths and relevant snippets
- Explicitly say "I don't know" when the answer is not present
- Run entirely locally with no cloud dependencies

## What Augustus Cannot Do

Augustus is intentionally limited:

- It does not connect to the internet or external APIs
- It does not reason beyond the indexed files
- It does not handle binary files (images, videos, compiled code)
- It is not a web application or SaaS
- It will not invent answers when information is missing

## Installation

Augustus requires Python 3.9 or later.

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/augustus.git
cd augustus
pip install -e .
```

## Usage

### Index a folder

```bash
augustus index /path/to/your/project
```

This creates a local vector index of the folder's contents.

### Ask questions

```bash
augustus ask "What does this project do?"
```

```bash
augustus ask "Where is the authentication logic?"
```

```bash
augustus ask "What technologies are used in this project?"
```

### View indexed files

```bash
augustus list
```

## Evidence-First Behavior

Augustus only answers using information found in the indexed files. If a question cannot be answered from the available context, Augustus will say so clearly rather than speculate.

All answers include citations showing which files were used as evidence.

## Limitations

- Augustus indexes text files only
- Large files may be chunked, which can affect context
- Semantic retrieval quality depends on the embedding model
- Questions requiring reasoning across many files may be harder to answer
- No support for real-time file watching or incremental updates yet

## License

MIT
