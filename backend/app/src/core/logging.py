import os
import sys

from app.src.core.settings import settings
from loguru import logger as loguru_logger

LOG_PATH = os.path.join(settings.LOG_PATH, f"log_{settings.PROJECT_NAME.lower()}.log")

loguru_logger.remove()
logger = loguru_logger.bind(name="general_logger")

logger.add(
    sink=LOG_PATH,
    format="{time} {level} {message}",
    level=settings.LOG_LEVEL,
    # rotation="3 MB",
    enqueue=True,
    colorize=True,
)  # retention="5 days")  #, compression="zip")  # , rotation="500 KB)"
logger.add(sys.stderr, level=settings.LOG_LEVEL.upper())
logger.info(f"Service {settings.PROJECT_NAME} started general logging to {LOG_PATH}")