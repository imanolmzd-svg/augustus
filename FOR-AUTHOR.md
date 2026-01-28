## FOR-AUTHOR — Augustus Ingestion Foundation

This project is intentionally small. The core idea is simple: point Augustus at a
folder, have it understand what is there, and only answer questions using evidence
from those files. This document explains how the ingestion foundation works, why
it was built this way, and what to watch out for as you extend it.

### Architecture in plain language

Think of ingestion as a careful librarian:

1. **Walk the shelves** (filesystem traversal)
2. **Ignore junk** (ignore rules)
3. **Open the book** (load text)
4. **Attach a label** (metadata + stable id)

The code keeps those steps in separate modules so each stays simple and testable.

### How the pieces connect

- `src/augustus/cli.py` is the front door. It parses arguments and prints output.
  It never contains business logic.
- `src/augustus/ingest/index.py` is the orchestration layer. It calls the loader
  and returns a summary for the CLI.
- `src/augustus/ingest/loader.py` loads files as text and produces `LoadedDocument`
  objects (content + metadata + stable id).
- `src/augustus/utils/file_tree.py` does the recursive walk and produces a
  deterministic list of file records.
- `src/augustus/utils/ignore.py` owns ignore rules and gitignore-style matching.
  Everything else delegates to it.

This split keeps responsibilities clear:
CLI → ingest orchestration → loader → utilities. No circular imports. No LangChain
in utilities.

### Why these technical decisions

- **Deterministic traversal**: Sorting by relative path makes output stable. This
  keeps future tests predictable and avoids “it worked on my machine” issues.
- **Ignore rules in one place**: The matcher lives in `utils/ignore.py` to prevent
  inconsistent behavior across modules.
- **Safe loading**: Binary detection (null bytes) and UTF-8 decoding avoid crashes.
  Size limits prevent enormous files from blowing up memory.
- **Stable document ids**: We hash `relative_path + content` so IDs change only
  when the file changes, not because of the absolute path on disk.

These choices emphasize correctness and predictability over cleverness.

### Key data structures

- `FileRecord` (in `utils/file_tree.py`) holds the normalized file view:
  absolute path, relative path, size, extension.
- `LoadedDocument` (in `ingest/loader.py`) holds the content and metadata.

Keeping these small and explicit prevents hidden behavior.

### Common pitfalls and how to avoid them

- **Counting ignored files**: Ignored directories can hide many files. The current
  counters reflect what the traversal actually visits, not every file on disk.
  If you later need “true total” counts, you will need a different strategy.
- **Binary detection is tricky**: Null-byte checks are fast, but not perfect.
  If a valid text file contains null bytes, it will be skipped. If you need more
  nuance, add a richer detector (but keep it deterministic).
- **Encoding assumptions**: We assume UTF-8. This keeps behavior predictable,
  but you may want configurable encodings later. If you add that, keep a strict
  fallback to avoid partial or corrupted reads.
- **Performance on huge repos**: Default ignores exist to skip big folders like
  `.git` or `node_modules`. If you remove them, ingestion will slow down quickly.

### Lessons learned

1. **Keep the boundary clean**: The CLI should not do work. It should report
   work done elsewhere. This makes the tool easy to script and test.
2. **Prefer small, explicit helpers**: `FileRecord` and `LoadedDocument` are
   deliberately simple. This keeps future refactors straightforward.
3. **Make safety the default**: Skipping unknown or unreadable files is safer
   than crashing. Augustus should be resilient on messy folders.

### Where to extend next

- Plug in chunking and embeddings in `ingest/` without changing `utils/`.
- Add `.augustusignore` support in `utils/ignore.py`.
- Add richer metadata (line counts, language guesses) in `ingest/loader.py`,
  but only if it stays deterministic.

If you keep those principles, Augustus will remain small, clear, and reliable.
