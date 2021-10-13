import logging
import sys

logger = logging.getLogger("__name__")
logging.basicConfig( level=logging.INFO)

def log(msg):
    logger.info(f"{msg}")
