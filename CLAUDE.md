# CLAUDE.md — Augustus

This file defines how Claude should work on the Augustus project.
Follow these instructions strictly.

---

## Project Overview

Augustus is a **small, local-first CLI tool** that helps users understand and query the contents of a folder.

It:
- indexes a folder’s structure and text files
- builds a local semantic index
- answers questions **only using evidence from the files**
- explicitly says “I don’t know” when the answer is not present

Augustus is intentionally **small and focused**.

---

## What Augustus Is Not

Do NOT turn Augustus into:
- a web application
- a SaaS
- a generic PDF chatbot
- an experiment playground

Avoid scope creep.

---

## Core Principles (Non-Negotiable)

1. **Evidence-first**
   - Never invent answers
   - Never use outside knowledge
   - Only reason from indexed files

2. **Folder as source of truth**
   - All context comes from the folder
   - File tree and file content are equally important

3. **CLI-first UX**
   - Clear commands
   - Predictable output
   - Readable formatting

4. **Small > Clever**
   - Prefer explicit, boring code
   - Avoid unnecessary abstractions

---

## Technology Constraints

- Language: **Python**
- CLI: **Typer**
- Orchestration: **LangChain**
- Vector store: **local (FAISS or Chroma)**
- No external databases
- No cloud dependencies by default

---

## Repository Structure

Expected layout:

src/augustus/
cli.py # CLI entrypoint only
ingest/ # folder loading, chunking, embeddings
qa/ # retrieval, prompts, answers
utils/ # helpers (no LangChain logic)
config.py # configuration and defaults
docs/
tests/
examples/


Rules:
- CLI never contains business logic
- `utils/` must not depend on LangChain
- Ingestion and QA are separate concerns
- No circular imports

---

## RAG Rules

- Always retrieve before answering
- Answers must be grounded in retrieved context
- If the answer is not present: say so clearly
- Cite sources using file paths and short snippets
- Avoid speculative language (“probably”, “likely”)

Baseline prompt concept:
> Answer only using the provided file context.  
> If the information is not present, say you do not know.

---

## Documentation Rules

When writing documentation:
- Be concise and factual
- Avoid hype and marketing language
- Prefer examples over explanation
- Do not document features that do not exist

README structure:
1. What Augustus is
2. Why it exists
3. What it can and cannot do
4. Installation
5. Basic usage
6. Limitations

---

## Commit Guidelines

Use conventional commits (lightweight):

- feat: new functionality
- fix: bug fix
- refactor: internal restructuring
- docs: documentation only
- test: adding or updating tests
- chore: tooling or setup

Rules:
- One logical change per commit
- Short, descriptive messages
- No “wip” or vague commits

---

## How to Work on This Project

When implementing features:
1. Keep changes small
2. Follow the existing structure
3. Update docs if behavior changes
4. Prefer correctness over cleverness

If something is unclear:
- Ask before assuming
- Do not invent requirements

---

## Definition of Done

A task is complete when:
- Code follows the project structure
- Behavior is deterministic
- No hallucinations are possible
- CLI output is clear
- Documentation is accurate

---

For every project, write a detailed FOR-AUTHOR.md file that explains the whole project in plain language. 

Explain the technical architecture, the structure of the codebase and how the various parts are connected, the technologies used, why we made these technical decisions, and lessons I can learn from it (this should include the bugs we ran into and how we fixed them, potential pitfalls and how to avoid them in the future, new technologies used, how good engineers think and work, best practices, etc). 

It should be very engaging to read; don't make it sound like boring technical documentation/textbook. Where appropriate, use analogies and anecdotes to make it more understandable and memorable.