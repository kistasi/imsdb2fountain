# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Downloads all screenplay scripts from imsdb.com and converts them to [Fountain](https://fountain.io) format. Crawling and parsing are separate phases.

## Running

The standard way to run is via Docker (mounts `downloaded-scripts/` as a volume so output persists):

```bash
source run.sh
```

To run directly without Docker (requires Python 3 + dependencies installed):

```bash
pip install -r requirements.txt
python main.py
```

## Architecture

Three modules with distinct responsibilities:

- **`crawler.py`** — fetches imsdb.com, scrapes all script links from `/all-scripts.html`, downloads each HTML script page, and writes raw text to `downloaded-scripts/<title>.fountain`.
- **`parser.py`** — reads a `.fountain` file, parses it with `screenplay-tools`, normalises ACTION elements (collapses whitespace), and rewrites the file using the Fountain writer.
- **`main.py`** — entry point; currently only calls `parse()` (crawler is imported but `get_all_scripts()` is not called from main).

The `downloaded-scripts/` directory is gitignored except for `.gitkeep`; `2012.fountain` in the repo root is a test fixture used during parser development.

## Key dependency

`screenplay-tools` (`screenplay_tools.fountain`) provides `Parser`, `Writer`, and `ElementType`. The `Parser` populates a `.script` object whose `.elements` list is iterated to manipulate element text before writing.
