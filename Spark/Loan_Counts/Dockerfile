# Using spark container so spark-submit can be executed
FROM bitnami/spark

USER root

WORKDIR /jump-start-spark

# Install zip, to bundle all python jobs into a zip
RUN apt-get update && apt-get install -y zip

# Create py-apps sub folder
WORKDIR /jump-start-spark/py-apps
# Copy the python files that are used to run applications on the spark cluster
COPY py-apps/Spark_Loan_Counts.py .

# Package all py-apps into a zip
# RUN zip -r ./py-apps/bundled-apps.zip ./py-apps/*.py

# create dependencies sub folder
WORKDIR /jump-start-spark/dependencies
# go back to main folder
WORKDIR /jump-start-spark

# Install the python dependencies into the dependencies folder
COPY requirements.txt .
#RUN pip install --no-cache-dir -t /jump-start-spark/dependencies -r requirements.txt
# package the dependencies in a zip
#RUN zip -r /jump-start-spark/dependencies.zip /jump-start-spark/dependencies

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN venv-pack -o pyspark_venv.tar.gz

RUN export PYSPARK_PYTHON=./environment/bin/python

#ENTRYPOINT start-slave spark://spark-master:7077

# Submit the spark applications if the spark cluster is available
ENTRYPOINT spark-submit  \
	--master local \
    --class org.apache.spark.examples.SparkPi\
	--name py-loans \
	####CONFIGS####
	--conf "spark.jars.ivy=/tmp/.ivy"\
	# configurations for PySpark connection to cassandra
	# this extension doesn't work despite being used in the documentation of cassandra:
	# https://github.com/datastax/spark-cassandra-connector/blob/master/doc/15_python.md
	#--conf "spark.sql.extensions=com.datastax.spark.connector.CassandraSparkExtensions"\
	# hostname of the cassandra service
	--conf "spark.cassandra.connection.host=cassandra-release.legerible-cassandra.svc.cluster.local"\
	# username to connect to cassandra
	--conf "spark.cassandra.auth.username=cassandra-legerible" \
	# password to connect to cassandra
	--conf "spark.cassandra.auth.password=ChangeThis"\
	####PACKAGES####
	--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2\
	--packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 \
	--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
	--archives pyspark_venv.tar.gz#environment \
	/jump-start-spark/py-apps/Spark_Loan_Counts.py

RUN echo "Spark-submit was executed"
	