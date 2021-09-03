# this file is executed when the kafka consumer container is started
# goal of the consumer is to read data from kafka streams
import psycopg2
import psycopg2.extras
from kafka import KafkaConsumer
from time import sleep
from json import loads
from book import Book
import logging

# Init Kafka Producer with specific cluster config
consumer = KafkaConsumer(
    # the topic we want to read
    'book_stream_topic',
    # name definied in /k8s/start_kafka.yaml
    bootstrap_servers=['kafka-release.legerible-kafka.svc.cluster.local:9092'],
    # convert all consumed data from json to python native
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    # when restarting the container, the consumer starts at the latest unread message to account for restarts of the
    # container and missed book ids being less troubling than adding the same book multiple times
    auto_offset_reset='latest',
    enable_auto_commit=False
)


def exec_statement(sql: str):
    """
        can execute every kind of Sql-statement but does NOT return a response.

        Use for:
            - CALL Procedure
            - UPDATE Statement
        :param sql:
        :return:
        """
    try:
        psycopg2_connection = psycopg2.connect(database="postgres", user="postgres", port=5432,
                                               password="1234", host="database")
        db_cursor = psycopg2_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        db_cursor.execute(sql)
        psycopg2_connection.commit()
        db_cursor.close()

        return True
    except psycopg2.errors.InFailedSqlTransaction:
        logging.error("Transaction Failed - Review given inputs!")
        return False
        
def add_new_book(obj_book):
    try:
        call = obj_book.get_s_sql_call()
        exec_statement(call)
        logging.info(f"Added book {obj_book.isbn} to postgres")
    except Exception as an_exception:
        logging.warning(an_exception)
        logging.warning("Book couldn't be added.")
        return False
    return True

def add_book_to_database(isbn):
    new_book = Book()
    new_book.set_via_isbn(isbn)
    add_new_book(new_book)


for payload in consumer:
    try:
        add_book_to_database(payload.value.get("isbn"))
    except:
        print("Book couldn't be added")
    # print(
    #     f"################ \n \
    #     Received payload: {payload.value.get('isbn')} \n \
    #     ################"
    # )
    # sleep between different API calls to collect isbn book data
    # otherwise we might get blocked
    sleep(5)
