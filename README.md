# imsdb2fountain

Downloads all screenplay scripts from [imsdb.com](http://www.imsdb.com), converts them to [Fountain](https://fountain.io) format using Claude AI, and exports them to PDF using [screenplain](https://github.com/vilcans/screenplain).

Based on the original project by [j2kun](https://github.com/j2kun/imsdb_download_all_scripts).

## Pipeline

1. **Crawl** — scrapes all script pages from imsdb.com and saves raw text to `downloaded-scripts/`
2. **Parse** — sends each file to `claude-haiku-4-5`, which cleans up scrape artifacts and normalises Fountain formatting while preserving the original text verbatim
3. **Convert** — renders each cleaned `.fountain` file to PDF via screenplain, with bold+underlined scene headings, page numbers, and scene numbers in the margins

Output PDFs are written to `output/`.

## Prerequisites

- Python 3
- An [Anthropic API key](https://console.anthropic.com)

## Usage

```bash
cp .env.example .env
# add your ANTHROPIC_API_KEY to .env

make run   # crawl → parse → convert
make clean # remove downloaded-scripts/ and output/
```
