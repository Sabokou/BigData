# import sqlalchemy
import psycopg2

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType, StructType, TimestampType

windowDuration = '5 minutes'
slidingDuration = '1 minute'
# Example Part 1
# Create a spark session
spark = SparkSession.builder.appName("Data Streaming").getOrCreate()

# Set log level
spark.sparkContext.setLogLevel('WARN')


# currently the important table that you may want to access is the "book_recommendation" table
# The schema of that table is:
#   transaction_id int,
#   user_id int,
#   loaned_book_id int,
#   recommended_book_id int,
#   PRIMARY KEY(transaction_id)
#
# The fields of that table are just preliminary and you are welcome to change them in k8s/start_cassandra.yaml


# Example Part 2
# Read messages from Kafka
kafkaMessages = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers",
            "kafka-release.legerible-kafka.svc.cluster.local:9092") \
    .option("subscribe", "book_loan_topic") \
    .load()
# .option("startingOffsets", "earliest") \


print("kafkaMessages", kafkaMessages)

# Define schema of tracking data
trackingMessageSchema = StructType() \
    .add("user_id", IntegerType()) \
    .add("book_id", IntegerType()) \
    .add("timestamp", IntegerType())

# Example Part 3
# Convert value: binary -> JSON -> fields + parsed timestamp

trackingMessages = kafkaMessages.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

tracking_messages_df = trackingMessages.select(
    # Extract 'value' from Kafka message (i.e., the tracking data)
    from_json(
        trackingMessages.value,
        trackingMessageSchema
    ).alias("json")
)
print("tracking_messages_df", tracking_messages_df)

messages_df = tracking_messages_df.select(
    # Convert Unix timestamp to TimestampType
    from_unixtime(col('json.timestamp'))
        .cast(TimestampType())
        .alias("parsed_timestamp"),

    # Select all JSON fields
    col("json.*")
) \
    .withColumnRenamed('json.book_id', 'book_id') \
    .withColumnRenamed('json.user_id', 'user_id') \
    .withWatermark("parsed_timestamp", windowDuration)

print("messages_df", messages_df)

# Example Part 4
# Compute most popular slides
popular = messages_df.groupBy(
    window(
        col("parsed_timestamp"),
        windowDuration,
        slidingDuration
    ),
    col("book_id")
).count().withColumnRenamed('count', 'views')

# Example Part 5
# Start running the query; print running counts to the console

consoleDump = popular \
    .writeStream \
    .trigger(processingTime=slidingDuration) \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .start()


# Example Part 6

def save_to_database(batchDataframe, batchId):
    # Define function to save a dataframe to mysql
    def save_to_db(iterator):
        # Connect to database and use schema
        psycopg2_connection = psycopg2.connect(database="postgres", user="postgres", port=5432,
                                               password="1234", host="database")
        db_cursor = psycopg2_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        for row in iterator:
            # Run upsert (insert or update existing)
            sql = f"""INSERT INTO KPI
                      (n_book_id, n_count) VALUES ({row.book_id}, {row.views})
                      ON CONFLICT (n_book_id) DO UPDATE
                      SET count={row.views}"""

            db_cursor.execute(sql)
            psycopg2_connection.commit()

        db_cursor.close()

    def save_to_cassandra(spark_df, cass_table, cass_keyspace="legerible"):
        """
        Append a spark dataframe to an existing cassandra table.

        Param
        ----
        spark_df: dataframe in pyspark dataframe format. Pandas dataframes are not supported, but you may convert them.
        cass_table: name of the table in the cassandra database e.g. "book_recommendation"
        cass_keyspace: name of the keyspace in which the table resides e.g. "legerible"
        """
        spark_df.write \
            .format("org.apache.spark.sql.cassandra") \
            .mode("append") \
            .options(table=cass_table, keyspace=cass_keyspace) \
            .save()

    # Perform batch UPSERTS per data partition
    batchDataframe.foreachPartition(save_to_db)
    save_to_cassandra(batchDataframe, "loan_counts")


# Example Part 7


dbInsertStream = popular.writeStream \
    .trigger(processingTime=slidingDuration) \
    .outputMode("update") \
    .foreachBatch(save_to_database) \
    .start()

# Wait for termination
spark.streams.awaitAnyTermination()
print("...working")
