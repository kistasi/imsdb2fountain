import time

from bs4 import BeautifulSoup

from helpers import db, imsdb, log


def step_01_shortlist_all():
    soup = BeautifulSoup(imsdb.get(imsdb.BASE_URL + "/all-scripts.html"), "html.parser")
    time.sleep(imsdb.REQUEST_DELAY)

    count = 0
    for p in soup.find_all("p"):
        if not p.a:
            continue
        title = p.a.get_text(strip=True)
        link = p.a["href"]
        db.upsert_shortlisted(title, link)
        count += 1

    log.info(f"shortlisted {count} screenplays")
