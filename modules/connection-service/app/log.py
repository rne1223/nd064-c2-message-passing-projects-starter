import logging
import sys

logger = logging.getLogger("__name__")
logging.basicConfig( level=logging.DEBUG)
# h1 = logging.StreamHandler(sys.stdout)
# h1.setLevel(logging.DEBUG)
# logger.addHandler(h1)
# h2 = logging.StreamHandler(sys.stderr)
# h2.setLevel(logging.ERROR)
# logger.addHandler(h2)

def log(msg):
    logger.info(f"{msg}")