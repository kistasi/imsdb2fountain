import codecs
import os
from pathlib import Path

from screenplain.export import pdf
from screenplain.export.pdf import Settings
from screenplain.parsers import fountain

SCRIPTS_DIR = "downloaded-scripts"
OUTPUT_DIR = "output"


def convert_file(src_path, out_dir):
    stem = Path(src_path).stem
    with codecs.open(src_path, "r", encoding="utf-8") as f:
        screenplay = fountain.parse(f)

    pdf_path = out_dir / f"{stem}.pdf"
    settings = Settings(strong_slugs=True)
    with open(pdf_path, "wb") as f:
        pdf.to_pdf(screenplay, f, settings=settings)


def convert():
    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(exist_ok=True)

    for filename in os.listdir(SCRIPTS_DIR):
        if filename.endswith(".fountain"):
            print(f"converting {filename}")
            try:
                convert_file(os.path.join(SCRIPTS_DIR, filename), out_dir)
            except Exception as e:
                print(f"  error: {e}")
