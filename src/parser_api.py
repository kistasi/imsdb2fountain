import os
from pathlib import Path

import anthropic

import db

SCRIPTS_DIR = "downloaded-scripts"

SYSTEM_PROMPT = (Path(__file__).parent / "system_prompt.md").read_text(encoding="utf-8")

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def parse_file(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    client = _get_client()

    with client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=64000,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": content}],
    ) as stream:
        output = stream.get_final_message()

    text = next((b.text for b in output.content if b.type == "text"), "")

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def parse_api():
    pending = {row["title"] for row in db.get_by_status("downloaded")}
    pending |= {row["title"] for row in db.get_by_status("failed")}

    for filename in os.listdir(SCRIPTS_DIR):
        if not filename.endswith(".fountain"):
            continue
        title = filename.removesuffix(".fountain")
        if title not in pending:
            continue

        print(f"parsing {filename}")
        try:
            parse_file(os.path.join(SCRIPTS_DIR, filename))
            db.set_status(title, "parsed")
        except Exception as e:
            print(f"  error: {e}")
            db.set_status(title, "failed", str(e))
