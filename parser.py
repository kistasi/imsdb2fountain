import os

from screenplay_tools.fountain.parser import ElementType, Parser
from screenplay_tools.fountain.writer import Writer


def parse():
    file = os.path.join("downloaded-scripts", "2012.fountain")
    with open(file, encoding="utf-8") as f:
        content = f.read()

    fp = Parser()
    fp.add_text(content)

    for element in fp.script.elements:
        if element.type is ElementType.ACTION:
            element._text = " ".join(element.text.split())

    writer = Writer()
    output = writer.write(fp.script)

    with open(file, "w", encoding="utf-8") as f:
        f.write(output)
