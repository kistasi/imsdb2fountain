# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Downloads all screenplay scripts from imsdb.com and converts them to [Fountain](https://fountain.io) format. Crawling and parsing are separate phases.

## Running

The standard way to run is via Docker (mounts `downloaded-scripts/` as a volume so output persists):

```bash
make build   # build the image
make run     # run the container
make all     # build + run in one step
make shell   # open a shell inside the container for debugging
make clean   # delete all files in downloaded-scripts/
```

To run directly without Docker (requires Python 3 + dependencies installed):

```bash
pip install -r requirements.txt
python src/main.py
```

## Architecture

Python source lives in `src/`. Three modules with distinct responsibilities:

- **`src/crawler.py`** — fetches imsdb.com, scrapes all script links from `/all-scripts.html`, downloads each HTML script page, and writes raw text to `downloaded-scripts/<title>.fountain`.
- **`src/parser.py`** — exposes `parse_file(path)` (single file) and `parse()` (all `.fountain` files in `downloaded-scripts/`); parses with `screenplay-tools`, normalises ACTION elements (collapses whitespace), and rewrites each file using the Fountain writer.
- **`src/main.py`** — entry point; currently calls `get_all_scripts()` to crawl (`parse()` is imported but commented out).

The `downloaded-scripts/` directory is gitignored except for `.gitkeep`; `2012.fountain` in the repo root is a test fixture used during parser development.

## Key dependency

`screenplay-tools` (`screenplay_tools.fountain`) provides `Parser`, `Writer`, and `ElementType`. The `Parser` populates a `.script` object whose `.elements` list is iterated to manipulate element text before writing.
