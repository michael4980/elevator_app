import logging
import colorlog


logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)


log_format = "%(log_color)s%(asctime)s %(levelname)s: %(message)s%(reset)s"
date_format = "%Y-%m-%d %H:%M:%S"

color_formatter = colorlog.ColoredFormatter(
    log_format,
    date_format,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    reset=True,
    style="%",
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(color_formatter)
logger.addHandler(console_handler)
