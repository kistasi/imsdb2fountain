from helpers import db
from steps._01_shortlister import shortlist_all
from steps._02_downloader import download_all
from steps._03a_parser_api import parse_api
from steps._03b_parser_claude_code import parse_claude_code
from steps._04_converter import convert

if __name__ == "__main__":
    db.init()
    shortlist_all()
    # download_all()
    # parse_api()
    # convert()
    print(db.summary())
