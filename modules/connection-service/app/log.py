import logging
import sys

logger = logging.getLogger("__name__")
logging.basicConfig(level=logging.INFO)
# h1 = logging.StreamHandler(sys.stdout)
# h1.setLevel(logging.DEBUG)
# logger.addHandler(h1)
# h2 = logging.StreamHandler(sys.stderr)
# h2.setLevel(logging.ERROR)
# logger.addHandler(h2)

# class NoParsingFilter(logging.Filter):
#     def filter(self, record):
#         return not record.getMessage().find('kafka')

# logger.addFilter(NoParsingFilter())

def log(msg):
    logger.info(f"{msg}")