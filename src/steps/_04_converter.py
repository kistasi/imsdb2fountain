import codecs
import os
from pathlib import Path

from screenplain.export import pdf
from screenplain.export.pdf import Settings
from screenplain.parsers import fountain
from screenplain.richstring import parse_emphasis
from screenplain.types import Slug

from helpers import db

SCRIPTS_DIR = "downloaded-scripts"
OUTPUT_DIR = "output"


def convert_file(src_path, out_dir):
    stem = Path(src_path).stem
    with codecs.open(src_path, "r", encoding="utf-8") as f:
        screenplay = fountain.parse(f)

    scene_num = 1
    for para in screenplay.paragraphs:
        if isinstance(para, Slug) and para.scene_number is None:
            para.scene_number = parse_emphasis(str(scene_num))
            scene_num += 1

    pdf_path = out_dir / f"{stem}.pdf"
    settings = Settings(strong_slugs=True)
    with open(pdf_path, "wb") as f:
        pdf.to_pdf(screenplay, f, settings=settings)


def step_04_convert():
    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(exist_ok=True)

    pending = {row["title"] for row in db.get_by_status("parsed")}
    pending |= {row["title"] for row in db.get_by_status("failed")}

    for filename in os.listdir(SCRIPTS_DIR):
        if not filename.endswith(".fountain"):
            continue
        title = filename.removesuffix(".fountain")
        if title not in pending:
            continue

        print(f"converting {filename}")
        try:
            convert_file(os.path.join(SCRIPTS_DIR, filename), out_dir)
            db.set_status(title, "converted")
        except Exception as e:
            print(f"  error: {e}")
            db.set_status(title, "failed", str(e))
