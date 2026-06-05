import time

import requests
from bs4 import BeautifulSoup

from helpers import db

BASE_URL = "http://www.imsdb.com"
REQUEST_DELAY = 1.0


def _get(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def shortlist_all():
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
