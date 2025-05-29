
# Design Decisions

## Goal

Build a simple, extensible validation and profiling tool for tabular data using the pandas ecosystem.

## Architecture

- `core.py` handles all validations and statistics.
- `loaders.py` handles data ingestion (CSV, Parquet, SQL).
- `reporters.py` generates markdown output.
- `tests/` provides 80+ % test coverage.

## Validation Rules

- Required columns: `id`, `name`, `score`
- ID uniqueness check
- Score range: 0–100
- No nulls in required columns

All checks return a structured dictionary with detailed stats and `validations`.

## Why Markdown?

- Easy to version control
- Easy to read and convert to HTML or PDF
- Integrates well in GitHub, GitLab, or Confluence
