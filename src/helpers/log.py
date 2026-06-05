import logging
import sys
from pathlib import Path

_LOG_PATH = Path(__file__).parent.parent.parent / "pipeline.log"

_logger = logging.getLogger("imsdb2fountain")
_logger.setLevel(logging.DEBUG)
_logger.propagate = False

_file_handler = logging.FileHandler(_LOG_PATH, encoding="utf-8")
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
)

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.INFO)
_console_handler.setFormatter(logging.Formatter("%(message)s"))

_logger.addHandler(_file_handler)
_logger.addHandler(_console_handler)

debug = _logger.debug
info = _logger.info
warning = _logger.warning
error = _logger.error
