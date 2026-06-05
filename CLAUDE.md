# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Downloads all screenplay scripts from imsdb.com and converts them to [Fountain](https://fountain.io) format. Crawling and parsing are separate phases.

## Running

Copy `.env.example` to `.env` and add your `ANTHROPIC_API_KEY` before running.

```bash
make run     # creates .venv, installs deps, runs src/main.py; reads ANTHROPIC_API_KEY from .env
make clean   # delete all files in downloaded-scripts/
```

## Architecture

Python source lives in `src/`. Three modules with distinct responsibilities:

- **`src/crawler.py`** — fetches imsdb.com, scrapes all script links from `/all-scripts.html`, downloads each HTML script page, and writes raw text to `downloaded-scripts/<title>.fountain`.
- **`src/parser.py`** — exposes `parse_file(path)` (single file) and `parse()` (all `.fountain` files in `downloaded-scripts/`); sends each file to the Claude API (`claude-haiku-4-5`) with a detailed Fountain formatting system prompt, and overwrites the file with the cleaned output.
- **`src/main.py`** — entry point; currently calls `get_all_scripts()` to crawl (`parse()` is imported but commented out).

The `downloaded-scripts/` directory is gitignored except for `.gitkeep`.

## Key dependency

The `anthropic` Python SDK is used to call `claude-haiku-4-5` for converting raw scraped screenplay text into valid Fountain format. The API key is read from the `ANTHROPIC_API_KEY` environment variable.
