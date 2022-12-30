from kafka import KafkaConsumer, KafkaProducer
import json

def serializer(value):
    return json.dumps(value).encode()

producer = KafkaProducer(bootstrap_servers='broker:29092', value_serializer=serializer)

def produce(key, value):
    producer.send('events.taxonomy', value=value, key=str(key).encode())
    producer.flush()
