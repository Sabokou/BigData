# this file is executed when the kafka producer container is executed
# The goal of the producer is to stream data into the system
# it connects to kafka and streams random isbns into a kafka topic
# consumers can then consume the new isbns

from isbn_generator import ISBN_generator as isbn_gen
from kafka import KafkaProducer
