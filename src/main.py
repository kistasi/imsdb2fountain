from crawler import get_all_scripts
from parser_api import parse_api
from parser_claude_code import parse_claude_code

if __name__ == "__main__":
    get_all_scripts()
    parse_claude_code()
