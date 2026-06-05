import os
import re

from screenplay_tools.fountain.parser import Parser
from screenplay_tools.fountain.writer import Writer


SCRIPTS_DIR = "downloaded-scripts"

_EXTERIOR = re.compile(r'^EXTERIOR\b')
_INTERIOR = re.compile(r'^INTERIOR\b')


def _preprocess_line(line):
    stripped = line.lstrip('\t')
    tab_count = len(line) - len(stripped)
    if tab_count >= 3:
        stripped = _EXTERIOR.sub('EXT.', stripped)
        stripped = _INTERIOR.sub('INT.', stripped)
    return stripped


def parse_file(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    content = "\n".join(_preprocess_line(line) for line in content.splitlines())

    fp = Parser()
    fp.add_text(content)

    writer = Writer()
    writer.pretty_print = False
    output = writer.write(fp.script)

    with open(path, "w", encoding="utf-8") as f:
        f.write(output)


def parse():
    for filename in os.listdir(SCRIPTS_DIR):
        if filename.endswith(".fountain"):
            print(f"parsing {filename}")
            parse_file(os.path.join(SCRIPTS_DIR, filename))
