from sys import api_version
from kafka import KafkaConsumer
from log import log
from json import loads

TOPIC_NAME = 'items'
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER,
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')),
     api_version=(0,10,1))

for message in consumer: 
    for i in range(20): 
        log(f"New locations: {message.value}")

# TODO: Search DB for close connections