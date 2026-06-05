import os
import time
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

import db

BASE_URL = "http://www.imsdb.com"
SCRIPTS_DIR = "downloaded-scripts"
DOWNLOAD_LIMIT = 1  # HACK: remove to download all scripts
REQUEST_DELAY = 1.0  # seconds between requests


def _get(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def shortlist_all():
    """Scrape /all-scripts.html and record every screenplay in the DB."""
    soup = BeautifulSoup(_get(BASE_URL + "/all-scripts.html"), "html.parser")
    time.sleep(REQUEST_DELAY)

    count = 0
    for p in soup.find_all("p"):
        if not p.a:
            continue
        title = p.a.get_text(strip=True)
        link = p.a["href"]
        db.upsert_shortlisted(title, link)
        count += 1

    print(f"shortlisted {count} screenplays")


def _fetch_script_text(relative_link):
    """Return script text, or None if unavailable (no script, PDF-only, etc.)."""
    tail = relative_link.split("/")[-1]
    print(f"  fetching {tail}")

    front_soup = BeautifulSoup(_get(BASE_URL + quote(relative_link)), "html.parser")
    time.sleep(REQUEST_DELAY)

    centers = front_soup.find_all("p", align="center")
    if not centers or not centers[0].a:
        print(f"  {tail}: no script link")
        return None

    script_link = centers[0].a["href"]
    if not script_link.endswith(".html"):
        print(f"  {tail}: PDF only, skipping")
        return None

    script_soup = BeautifulSoup(_get(BASE_URL + script_link), "html.parser")
    time.sleep(REQUEST_DELAY)

    cells = script_soup.find_all("td", {"class": "scrtext"})
    if not cells:
        print(f"  {tail}: no script text")
        return None

    return cells[0].get_text()


def download_all():
    """Download raw script text for every shortlisted (or previously failed) screenplay."""
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
