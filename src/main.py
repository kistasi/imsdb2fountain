import db
from converter import convert
from crawler import download_all, shortlist_all
from parser_api import parse_api
from parser_claude_code import parse_claude_code

if __name__ == "__main__":
    db.init()
    shortlist_all()
    # download_all()
    # parse_api()
    # convert()
    print(db.summary())
