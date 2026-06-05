import requests

BASE_URL = "http://www.imsdb.com"
REQUEST_DELAY = 1.0


def get(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text
