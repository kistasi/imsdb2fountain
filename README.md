# imsdb2fountain

Downloads all screenplay scripts from [imsdb.com](http://www.imsdb.com) and converts them to [Fountain](https://fountain.io) format — a plain text markup language for screenwriters. Conversion is done by Claude AI, which cleans up scrape artifacts and normalises formatting while preserving the original text verbatim.

Based on the original project by [j2kun](https://github.com/j2kun/imsdb_download_all_scripts).

## Prerequisites

- Python 3
- An [Anthropic API key](https://console.anthropic.com)

## Usage

```bash
cp .env.example .env
# add your ANTHROPIC_API_KEY to .env

make run
```

Scripts are saved to `downloaded-scripts/`.
