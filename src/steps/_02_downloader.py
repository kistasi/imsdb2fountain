import os
import time
from urllib.parse import quote

from bs4 import BeautifulSoup

from helpers import db, imsdb

SCRIPTS_DIR = "downloaded-scripts"
DOWNLOAD_LIMIT = 1  # HACK: remove to download all scripts


def _fetch_script_text(relative_link):
    tail = relative_link.split("/")[-1]
    print(f"  fetching {tail}")

    front_soup = BeautifulSoup(
        imsdb.get(imsdb.BASE_URL + quote(relative_link)), "html.parser"
    )
    time.sleep(imsdb.REQUEST_DELAY)

    centers = front_soup.find_all("p", align="center")
    if not centers or not centers[0].a:
        print(f"  {tail}: no script link")
        return None

    script_link = centers[0].a["href"]
    if not script_link.endswith(".html"):
        print(f"  {tail}: PDF only, skipping")
        return None

    script_soup = BeautifulSoup(imsdb.get(imsdb.BASE_URL + script_link), "html.parser")
    time.sleep(imsdb.REQUEST_DELAY)

    cells = script_soup.find_all("td", {"class": "scrtext"})
    if not cells:
        print(f"  {tail}: no script text")
        return None

    return cells[0].get_text()


def step_02_download_all():
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    pending = db.get_by_status("shortlisted") + db.get_by_status("failed")
    if not pending:
        print("nothing to download")
        return

    downloaded = 0
    for row in pending:
        if downloaded >= DOWNLOAD_LIMIT:
            break

        title = row["title"]
        link = row["imsdb_link"]
        print(f"downloading {title!r}")

        try:
            script = _fetch_script_text(link)
        except Exception as e:
            print(f"  error: {e}")
            db.set_status_by_link(link, "failed", str(e))
            continue

        if not script:
            db.set_status_by_link(link, "failed", "no script available")
            continue

        path = os.path.join(SCRIPTS_DIR, title + ".fountain")
        with open(path, "w", encoding="utf-8") as f:
            f.write(script)

        db.set_status_by_link(link, "downloaded")
        downloaded += 1
