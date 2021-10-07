from kafka import KafkaConsumer
from log import log

TOPIC_NAME = 'items'

consumer = KafkaConsumer(TOPIC_NAME)
for message in consumer:
    log(message)
