---
name: augustus-commit-conventions
description: Generate commit messages following the Augustus commit conventions. Apply when suggesting commit names, planning work, or summarizing changes.
---

# Commit Message Conventions

## Format
Use conventional commits (lightweight):

type: short description


## Allowed Types
- feat: new functionality
- fix: bug fix
- refactor: internal code change
- docs: documentation only
- test: adding or updating tests
- chore: tooling or setup

## Rules
- Description in present tense
- Lowercase
- Under ~60 characters
- One logical change per commit

## Examples
- `feat: add folder ingestion pipeline`
- `fix: ignore binary files during indexing`
- `docs: add quickstart section to README`
- `refactor: split retrieval logic from cli`

Avoid vague commits like:
- “update stuff”
- “fix bug”
- “wip”

The commit history should read like a clean narrative of the project.