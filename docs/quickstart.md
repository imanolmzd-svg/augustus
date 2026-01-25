# Quickstart Guide

Augustus is a local-first CLI tool for understanding and querying folder contents.

## Installation

Install Augustus in editable mode:

```bash
pip install -e .
```

## Basic Usage

### Index a folder

```bash
augustus index /path/to/your/project
```

This creates a local vector index of the folder's contents.

### Ask questions

```bash
augustus ask "What does this project do?"
```

### List indexed files

```bash
augustus list
```

## Next Steps

This guide will be expanded as features are implemented. See `architecture.md` for technical details.
