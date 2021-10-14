from sys import api_version
from kafka import KafkaConsumer, KafkaProducer
from log import log
from json import loads, dumps
from DB import Connections
from datetime import datetime

FORMAT = "%Y-%m-%d"
TOPIC_NAME = 'items'
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                        value_serializer=lambda x: dumps(x).encode('utf-8'),
                        api_version=(0,10,1))

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER,
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')),
     api_version=(0,10,1))


# startDate = datetime.strptime("2020-01-01","%Y-%m-%d")
# endDate = datetime.strptime("2020-12-30","%Y-%m-%d")
# connections = Connections.find_contacts(person_id=1, start_date=startDate,end_date=endDate)


connections = [] 
for message in consumer: 
    data = message.value

    person_id = data['person_id']
    start_date = datetime.strptime(data['start_date'], FORMAT)
    end_date = datetime.strptime(data['end_date'], FORMAT)

    connections = Connections.find_contacts(person_id, start_date, end_date)

#     log(connections)
#     data = {"foo---": f"{connections}" }
    producer.send('con', value=f"{connections}")

    # log(connections)

