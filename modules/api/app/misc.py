import logging
import sys

logger = logging.getLogger("__name__")
logging.basicConfig( level=logging.DEBUG)
h1 = logging.StreamHandler(sys.stdout)
h1.setLevel(logging.DEBUG)
h2 = logging.StreamHandler(sys.stderr)
h2.setLevel(logging.ERROR)
logger.addHandler(h1)
logger.addHandler(h2)

def log(msg):
    logger.info(f"{msg}")

# @app.before_request
def before_request():
    pass
    # # Set up a Kafka producer
    # TOPIC_NAME = 'items'
    # KAFKA_SERVER = 'localhost:9092'
    # producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    # # Setting Kafka to g enables us to use this
    # # in other parts of our application
    # g.kafka_producer = producer