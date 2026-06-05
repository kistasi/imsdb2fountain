import os
import time
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://www.imsdb.com"
SCRIPTS_DIR = "downloaded-scripts"
REQUEST_DELAY = 1.0  # seconds between requests


def _get(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def get_script(relative_link):
    tail = relative_link.split("/")[-1]
    print(f"fetching {tail}")

    front_soup = BeautifulSoup(_get(BASE_URL + quote(relative_link)), "html.parser")
    time.sleep(REQUEST_DELAY)

    centers = front_soup.find_all("p", align="center")
    if not centers or not centers[0].a:
        print(f"{tail} has no script :(")
        return None, None

    script_link = centers[0].a["href"]
    if not script_link.endswith(".html"):
        print(f"{tail} is a pdf :(")
        return None, None

    title = (
        script_link.split("/")[-1].removesuffix(" Script.html").removesuffix(".html")
    )
    script_soup = BeautifulSoup(_get(BASE_URL + script_link), "html.parser")
    time.sleep(REQUEST_DELAY)

    cells = script_soup.find_all("td", {"class": "scrtext"})
    if not cells:
        print(f"{tail} has no script text :(")
        return None, None

    return title, cells[0].get_text()


def get_all_scripts():
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    soup = BeautifulSoup(_get(BASE_URL + "/all-scripts.html"), "html.parser")
    time.sleep(REQUEST_DELAY)

    for p in soup.find_all("p"):
        if not p.a:
            continue
        title, script = get_script(p.a["href"])
        if not script:
            continue

        path = os.path.join(SCRIPTS_DIR, title.strip() + ".fountain")
        with open(path, "w", encoding="utf-8") as f:
            f.write(script)
