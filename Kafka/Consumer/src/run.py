# this file is executed when the kafka consumer container is started
# goal of the consumer is to read data from kafka streams

from kafka import KafkaConsumer
from time import sleep
from json import loads

# Init Kafka Producer with specific cluster config
consumer = KafkaConsumer(
    # the topic we want to read
    'book_stream_topic',
    # name definied in /k8s/start_kafka.yaml
    bootstrap_servers=['kafka-release.legerible-kafka.svc.cluster.local:9092'],
    # convert all consumed data from json to python native
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    # when restarting the container, the consumer starts at the earliest unread message
    auto_offset_reset='earliest',
    enable_auto_commit=False
)

for payload in consumer:
    print(
        f"################ \n \
        Received payload: {payload.value} \n \
        ################"
    )

