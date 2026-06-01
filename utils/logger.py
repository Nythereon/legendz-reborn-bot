import logging

logger = logging.getLogger("player_reborn")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("player_reborn.log")

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

