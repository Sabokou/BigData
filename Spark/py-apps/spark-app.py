# import findspark
# findspark.init()

# from pyspark import SparkContext
# from pyspark.streaming import StreamingContext
# from pyspark.streaming.kafka import KafkaUtils

# if __name__=="__main__":
#     sc = SparkContext(appName="Kafka Spark Streaming")
    
#     ssc = StreamingContext(sc, 60)

#     message=KafkaUtils.createDirectStream(ssc, topics=["testtopic"], kafkaParams={"metadata.broker.list":"kafka-release.legerible-kafka.svc.cluster.local:9092"})

#     words=message.map(lambda x: x[1]).flatMap(lambda x: x.split(" "))

#     wordcount= words.map(lambda x: (x,1)).reduceByKey(lambda a,b: a+b)

#     wordcount.pprint()

#     ssc.start()
#     ssc.awaitTermination()


from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType, StringType, StructType, TimestampType

# dbOptions = {"host": "database", 'port': 5432, "user": "postgres", "password": "1234"}
# dbSchema = 'postgres'
windowDuration = '5 minutes'
slidingDuration = '1 minute'
# Example Part 1
# Create a spark session
spark = SparkSession.builder.appName("Data Streaming").getOrCreate()

# Set log level
spark.sparkContext.setLogLevel('WARN')

# Example Part 2
# Read messages from Kafka
kafkaMessages = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers",
            "kafka-release.legerible-kafka.svc.cluster.local:9092") \
    .option("subscribe", "loan-book-topic") \
    .load()
    # .option("startingOffsets", "earliest") \
    

print("kafkaMessages", kafkaMessages)

# kafkaMessages.head()
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


# def saveToDatabase(batchDataframe, batchId):
#     # Define function to save a dataframe to mysql
#     def save_to_db(iterator):
#         # Connect to database and use schema
#         session = mysqlx.get_session(dbOptions)
#         session.sql("USE popular").execute()

#         for row in iterator:
#             # Run upsert (insert or update existing)
#             sql = session.sql("INSERT INTO popular "
#                               "(mission, count) VALUES (?, ?) "
#                               "ON DUPLICATE KEY UPDATE count=?")
#             sql.bind(row.mission, row.views, row.views).execute()

#         session.close()

    # Perform batch UPSERTS per data partition
    # batchDataframe.foreachPartition(save_to_db)

# Example Part 7

"""
dbInsertStream = postgres.writeStream \
    .trigger(processingTime=slidingDuration) \
    .outputMode("update") \
    .foreachBatch(saveToDatabase) \
    .start()
"""

# Wait for termination
spark.streams.awaitAnyTermination()
print("...working")
