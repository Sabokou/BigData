# this file is executed when the kafka producer container is executed
# The goal of the producer is to stream data into the system
# it connects to kafka and streams random isbns into a kafka topic
# consumers can then consume the new isbns

from isbn_generator import ISBN_generator as isbn_gen
from kafka import KafkaProducer
from time import sleep
from json import dumps

# Init Kafka Producer with specific cluster config
producer = KafkaProducer(
    # name definied in /k8s/start_kafka.yaml
    bootstrap_servers=['kafka-release.legerible-kafka.svc.cluster.local:9092'],
    # convert all produced data to json in UTF-8 encoding 
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

# Callback functions for successfully send messages
def on_success(metadata):
    print("Sending was successful")
    print("metadata:", metadata)

# Callback functions for failed messages
def on_error(exception):
    print("Sending message failed")
    print("Error:", exception)

# Generate data to send
ig = isbn_gen()

while True:
    isbn = ig.random_isbn()
    # Retrieve whole book information
    payload = {'isbn': isbn}

    # send the book info to the book_stream_topic topic
    producer.send('book_stream_topic', value=payload).add_callback(on_success).add_errback(on_error)

    # Only stream every 3 seconds
    sleep(3)

