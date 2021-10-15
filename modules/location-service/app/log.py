import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def log(msg):
    logger.info(f"{msg}")
