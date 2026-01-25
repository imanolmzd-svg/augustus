# Tests

This directory will contain the test suite for Augustus.

## Structure

Tests will be organized to mirror the source structure:

```
tests/
├── test_cli.py
├── test_config.py
├── ingest/
│   ├── test_loader.py
│   ├── test_splitter.py
│   └── test_index.py
├── qa/
│   ├── test_retriever.py
│   ├── test_prompt.py
│   └── test_answer.py
└── utils/
    ├── test_file_tree.py
    ├── test_ignore.py
    └── test_formatting.py
```

## Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=augustus --cov-report=html
```
