from helpers import db
from steps.converter import convert
from steps.downloader import download_all
from steps.parser_api import parse_api
from steps.parser_claude_code import parse_claude_code
from steps.shortlister import shortlist_all

if __name__ == "__main__":
    db.init()
    shortlist_all()
    # download_all()
    # parse_api()
    # convert()
    print(db.summary())
