from kafka import KafkaProducer

# TOPIC_NAME = 'items'
KAFKA_SERVER = 'localhost:9091'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

def sendMsg(msg, topic='items'):
    producer.sendt(topic,msg)
    producer.flush()
