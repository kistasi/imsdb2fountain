# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Downloads all screenplay scripts from imsdb.com, converts them to [Fountain](https://fountain.io) format, then exports to PDF using screenplain. Crawling, parsing, and conversion are separate phases.

## Running

Copy `.env.example` to `.env` and add your `ANTHROPIC_API_KEY` before running.

```bash
make run     # creates .venv, installs deps, runs src/main.py; reads ANTHROPIC_API_KEY from .env
make clean   # delete all files in downloaded-scripts/
```

## Architecture

Python source lives in `src/`. Three modules with distinct responsibilities:

- **`src/crawler.py`** — fetches imsdb.com, scrapes all script links from `/all-scripts.html`, downloads each HTML script page, and writes raw text to `downloaded-scripts/<title>.fountain`.
- **`src/parser_api.py`** / **`src/parser_claude_code.py`** — send each `.fountain` file to the Claude API (`claude-haiku-4-5`) with a detailed Fountain formatting system prompt and overwrite the file with cleaned output.
- **`src/converter.py`** — reads each cleaned `.fountain` file using screenplain's parser, auto-numbers any slugs that lack a scene number, then writes `output/<title>.pdf` with bold+underlined scene headings, page numbers, and margin scene numbers.
- **`src/main.py`** — entry point; runs crawl → parse → convert in sequence.

The `downloaded-scripts/` directory is gitignored except for `.gitkeep`. The `output/` directory is created on demand.

## Key dependency

The `anthropic` Python SDK is used to call `claude-haiku-4-5` for converting raw scraped screenplay text into valid Fountain format. The API key is read from the `ANTHROPIC_API_KEY` environment variable.
