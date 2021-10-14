import logging
import sys
from pprint import pformat

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)
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
    logger.info(f"{pformat(msg)}")