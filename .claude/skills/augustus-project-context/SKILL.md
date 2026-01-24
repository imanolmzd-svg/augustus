---
name: augustus-project-context
description: Core context and non-negotiable principles of the Augustus project. Apply whenever working on this repository, writing code, making design decisions, or answering questions about how Augustus should work.
---

# Augustus — Project Context

## What is Augustus
Augustus is a **small, local-first CLI tool** that helps users understand and query the contents of a folder.

It answers questions like:
- What is in this folder?
- What does this project do?
- Where is the main logic?
- What technologies are used?

## What Augustus is NOT
- Not a web app
- Not a SaaS
- Not a generic “chat with PDFs” product
- Not a playground for unrelated experiments

Keep the scope intentionally small and focused.

## Core Principles (Non-Negotiable)

### Evidence-first
- Augustus must **only answer using information found in the indexed files**
- If the information is not present, explicitly say: *“I don’t know based on the files.”*
- No hallucinations, no guessing, no filling gaps

### Folder-centric
- The folder is the source of truth
- All reasoning must be grounded in:
  - file tree
  - file contents
  - metadata derived from files

### CLI-first
- Augustus is primarily a command-line tool
- UX means: clear output, predictable commands, readable formatting

### Safe defaults
- Ignore binary files
- Ignore common junk folders (`node_modules`, `dist`, `venv`, `.git`, etc.)
- Never index secrets or environment files unless explicitly allowed

## Technology Direction
- Language: Python (modern, type-hinted)
- Orchestration: LangChain
- Interface: CLI (Typer or similar)
- Vector store: local (FAISS or Chroma)
- Designed to run locally, not in the cloud

All contributions must respect these constraints.