from sys import api_version
from kafka import KafkaConsumer
from log import log
from json import loads
from DB import ConnectionService 

TOPIC_NAME = 'items'
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER,
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')),
     api_version=(0,10,1))


connections = ConnectionService.find_contacts()

for connection in connections:
    log(f"Connection: {connection}")

# for person in persons:
#     log(f"Showing Person: {person.first_name}")

# for message in consumer: 
#     for i in range(2): 
#         log(f"New locations: {message.value}")

