from kafka import KafkaProducer
from app.misc import log

# TOPIC_NAME = 'items'
KAFKA_SERVER = 'udaconnect-connection-service:9091'

# producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

# def sendMsg(msg, topic='items'):
#     producer.sendt(topic,msg)
#     producer.flush()
