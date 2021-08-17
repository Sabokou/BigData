from kafka import KafkaProducer
from json import dumps


# Init Kafka Producer with specific cluster config
class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            # name defined in /k8s/start_kafka.yaml
            bootstrap_servers=['kafka-release.legerible-kafka.svc.cluster.local:9092'],
            # convert all produced data to json in UTF-8 encoding
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )

    # Callback functions for successfully send messages
    @staticmethod
    def on_success(metadata):
        print("Sending was successful")
        print("metadata:", metadata)

    # Callback functions for failed messages
    @staticmethod
    def on_error(exception):
        print("Sending message failed")
        print("Error:", exception)
