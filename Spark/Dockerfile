# Using spark container so spark-submit can be executed
FROM bitnami/spark

USER root

WORKDIR /jump-start-spark

# Install zip, to bundle all python jobs into a zip
RUN apt-get update && apt-get install -y zip

# Create py-apps sub folder
WORKDIR /jump-start-spark/py-apps
# Copy the python files that are used to run applications on the spark cluster
COPY py-apps/spark-app.py .

# Package all py-apps into a zip
# RUN zip -r ./py-apps/bundled-apps.zip ./py-apps/*.py

# create dependencies sub folder
WORKDIR /jump-start-spark/dependencies
# go back to main folder
WORKDIR /jump-start-spark

# Install the python dependencies into the dependencies folder
COPY requirements.txt .
RUN pip install --no-cache-dir -t /jump-start-spark/dependencies -r requirements.txt
# package the dependencies in a zip
RUN zip -r /jump-start-spark/dependencies.zip /jump-start-spark/dependencies

# Submit the spark applications if the spark cluster is available
ENTRYPOINT spark-submit --verbose \
	--master spark://spark-master:7077 \
	--class org.apache.spark.examples.SparkPi\
	--name py-app \
	--conf "spark.jars.ivy=/tmp/.ivy"\
	--py-files dependencies.zip\
	/jump-start-spark/py-apps/spark-app.py

RUN echo "Spark-submit was executed"
	
# example code from lecture:
# could be usefull to establish a connection with kafka

# FROM bitnami/spark:3.0.0
# LABEL maintainer="Dennis Pfisterer, http://dennis-pfisterer.de"
# WORKDIR /app

# #------------------------------------
# # Set execution environment

# # Java Dependencies for Spark Kafka
# # These are obtained using Ivy later
# ENV SPARK_VERSION "3.0.0"
# ENV SPARK_KAFKA_DEPENDENCY "org.apache.spark:spark-sql-kafka-0-10_2.12:${SPARK_VERSION}"
# ENV IVY_PACKAGE_DIR "/tmp/.ivy"

# #------------------------------------
# # Prepare the system

# USER root

# # Workaround for "failure to login" error message:
# # cf. https://stackoverflow.com/questions/41864985/hadoop-ioexception-failure-to-login/56083736
# RUN groupadd --gid 1001 spark
# RUN useradd --uid 1001 --gid spark --shell /bin/bash spark
# # End: Workaround

# RUN apt-get update && apt-get install -y zip
# RUN chown spark:spark /app/

# USER spark

# WORKDIR /app

# #------------------------------------
# # Prepare dependencies in ZIP file

# # Pre-Install Maven dependencies by running an empty python file using spark-submit
# # to benefit from Docker's build cache
# RUN touch /tmp/empty.py && spark-submit --verbose \
# 	--conf "spark.jars.ivy=${IVY_PACKAGE_DIR}" \
# 	--packages "${SPARK_KAFKA_DEPENDENCY}" \
# 	/tmp/empty.py && rm -f /tmp/empty.py

# # Prepare the app's python dependencies
# ADD --chown=spark:spark requirements.txt /app/
# RUN pip install --no-cache-dir -t /app/dependencies -r requirements.txt

# # Zip all dependencies
# WORKDIR /app/dependencies
# RUN zip -r /app/dependencies.zip .

# WORKDIR /app
# RUN rm -rf /app/dependencies

# #------------------------------------
# # Copy the application code into the container

# # Copy application code
# COPY --chown=spark:spark *.py /app/

# #------------------------------------
# # Set entrypoint and use dependencies zip file

# # Use YARN deployment in client mode (requires Hadoop config)
# # --master yarn --deploy-mode client"

# # Use YARN deployment in cluster mode (requires Hadoop config)
# # --master yarn --deploy-mode cluster

# # Use local deployment
# # --master local

# ENTRYPOINT spark-submit --verbose \
# 	--master local \
# 	--conf "spark.jars.ivy=${IVY_PACKAGE_DIR}" \
# 	--packages "${SPARK_KAFKA_DEPENDENCY}" \
# 	--py-files /app/dependencies.zip \
# 	/app/spark-app.py

# CMD [""]
