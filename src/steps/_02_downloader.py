import os
import time
from urllib.parse import quote

from bs4 import BeautifulSoup

from helpers import db, imsdb, log

SCRIPTS_DIR = "downloaded-scripts"


def _fetch_script_text(relative_link):
    tail = relative_link.split("/")[-1]
    log.debug(f"fetching {tail}")

    front_soup = BeautifulSoup(
        imsdb.get(imsdb.BASE_URL + quote(relative_link)), "html.parser"
    )
    time.sleep(imsdb.REQUEST_DELAY)

    centers = front_soup.find_all("p", align="center")
    if not centers or not centers[0].a:
        log.warning(f"{tail}: no script link")
        return None

    script_link = centers[0].a["href"]
    if not script_link.endswith(".html"):
        log.warning(f"{tail}: PDF only, skipping")
        return None

    script_soup = BeautifulSoup(imsdb.get(imsdb.BASE_URL + script_link), "html.parser")
    time.sleep(imsdb.REQUEST_DELAY)

    cells = script_soup.find_all("td", {"class": "scrtext"})
    if not cells:
        log.warning(f"{tail}: no script text")
        return None

    return cells[0].get_text()


def step_02_download_all():
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    pending = db.get_by_status("shortlisted") + db.get_by_status("failed")
    if not pending:
        log.info("nothing to download")
        return

    for row in pending:
        title = row["title"]
        link = row["imsdb_link"]
        log.info(f"downloading {title!r}")

        try:
            script = _fetch_script_text(link)
        except Exception as e:
            log.error(f"download failed for {title!r}: {e}")
            db.set_status_by_link(link, "failed", str(e))
            continue

        if not script:
            db.set_status_by_link(link, "failed", "no script available")
            continue

        path = os.path.join(SCRIPTS_DIR, title + ".fountain")
        with open(path, "w", encoding="utf-8") as f:
            f.write(script)

        db.set_status_by_link(link, "downloaded")
