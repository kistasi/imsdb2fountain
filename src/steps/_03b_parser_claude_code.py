import os
import subprocess
from pathlib import Path

SCRIPTS_DIR = "downloaded-scripts"

SYSTEM_PROMPT = (
    Path(__file__).parent.parent / "helpers" / "system_prompt.md"
).read_text(encoding="utf-8")


def parse_file(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    result = subprocess.run(
        [
            "claude",
            "-p",
            "--system-prompt",
            SYSTEM_PROMPT,
            "--no-session-persistence",
            "--tools",
            "",
        ],
        input=content,
        capture_output=True,
        text=True,
        check=True,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(result.stdout)


def step_03b_parse_claude_code():
    for filename in os.listdir(SCRIPTS_DIR):
        if filename.endswith(".fountain"):
            print(f"parsing {filename}")
            parse_file(os.path.join(SCRIPTS_DIR, filename))
