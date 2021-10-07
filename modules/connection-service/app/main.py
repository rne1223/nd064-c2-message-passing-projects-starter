from kafka import KafkaConsumer
from log import log

TOPIC_NAME = 'items'
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)

for message in consumer: 
    log(f"New locations: {message}")

# TODO: Search DB for close connections