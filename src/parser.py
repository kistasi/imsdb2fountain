import os

from screenplay_tools.fountain.parser import ElementType, Parser
from screenplay_tools.fountain.writer import Writer


SCRIPTS_DIR = "downloaded-scripts"


def parse_file(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    fp = Parser()
    fp.add_text(content)

    for element in fp.script.elements:
        if element.type is ElementType.ACTION:
            element._text = " ".join(element.text.split())

    writer = Writer()
    output = writer.write(fp.script)

    with open(path, "w", encoding="utf-8") as f:
        f.write(output)


def parse():
    for filename in os.listdir(SCRIPTS_DIR):
        if filename.endswith(".fountain"):
            print(f"parsing {filename}")
            parse_file(os.path.join(SCRIPTS_DIR, filename))
