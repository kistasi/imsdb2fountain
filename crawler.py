import os
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://www.imsdb.com"
SCRIPTS_DIR = "downloaded-scripts"


def get_script(relative_link):
    tail = relative_link.split("/")[-1]
    print("fetching %s" % tail)
    script_front_url = BASE_URL + quote(relative_link)
    front_page_response = requests.get(script_front_url)
    front_soup = BeautifulSoup(front_page_response.text, "html.parser")

    try:
        script_link = front_soup.find_all("p", align="center")[0].a["href"]
    except IndexError:
        print("%s has no script :(" % tail)
        return None, None

    if script_link.endswith(".html"):
        title = script_link.split("/")[-1].split(" Script")[0]
        script_url = BASE_URL + script_link
        script_soup = BeautifulSoup(requests.get(script_url).text, "html.parser")
        script_text = script_soup.find_all("td", {"class": "scrtext"})[0].get_text()
        return title, script_text
    else:
        print("%s is a pdf :(" % tail)
        return None, None


def get_all_scripts():
    response = requests.get(BASE_URL + "/all-scripts.html")
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")

    for p in paragraphs:
        relative_link = p.a["href"]
        title, script = get_script(relative_link)
        if not script:
            continue

        with open(
            os.path.join(SCRIPTS_DIR, title.strip(".html") + ".fountain"),
            "w",
            encoding="utf-8",
        ) as outfile:
            outfile.write(script)
