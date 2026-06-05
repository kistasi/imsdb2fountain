from helpers import db, log
from steps._01_shortlister import step_01_shortlist_all
from steps._02_downloader import step_02_download_all
from steps._03a_parser_api import step_03a_parse_api
from steps._03b_parser_claude_code import step_03b_parse_claude_code
from steps._04_converter import step_04_convert

if __name__ == "__main__":
    log.info("pipeline started")
    db.init()
    step_01_shortlist_all()
    step_02_download_all()
    step_03a_parse_api()
    step_04_convert()
    summary = db.summary()
    log.info(f"pipeline finished: {summary}")
