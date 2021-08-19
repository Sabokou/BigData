# BigData

This student project is part of our ...

## Table of Contents

---

1. [Use-Case](#Use-Case)
2. [Architecture and Design](#Architecture-an-Design)
3. [Folder Structure](#Folder-Structure)
4. [Setup Instructions](#Setup-Instructions)
5. [Screencast Demonstration](#Screencast-Demonstration)

---

<br>

## Use-Case

...

<br>

## Architecture and Design

...

<br>

## Folder Structure

<ul>

<li><b> Main folder </b></li>

In the main folder of this directory you can find skaffold.yaml. This file is used to create kubernetes artifacts like containers, deploys helm charts and starts all kubernetes ressources in the [k8s](k8s) folder. \
It also holds some Ressources that are used to build a container for the Webapp and a docker-compose.yml file that can be used to run part of the infrastructure in docker instead of Kubernetes, this is just for debugging purposes.


<li><b> k8s </b></li>

The k8s folder holds Kubernetes ressources like Services, LoadBalancer, Deployments and Pods. They are defined in YAML files. \
Multiple specifications for the same software are written in the same YAML file seperated by "---". This is helpfull when a deployment and a Service that reference the same Pod is used. 

You can read more about it [here](k8s/README.md).

<li><b> Kafka </b></li>

Kafka holds the resources for two pods: a Producer and a Consumer.\
The Producer streams randomly generated ISBN information into a Kafka topic, while the consumer reads from the same topic and dumps the information to the console. The Kafka cluster is created via a helm chart, you can find the specifics in [skaffold.yaml](skaffold.yaml). 

For more information on Kafka Ressources look [here](Kafka/README.md)

<li><b> Spark </b></li>

The Spark folder contains resources to build a container that prepares dependencies and submits them together with [spark-app.py](Spark/py-apps/spark-app.py) to the spark cluster, as created [here](skaffold.yaml).

For more information on Spark click [here](Spark/README.md).

<li><b> Webapp </b></li>

The Webapp contains the resources for a Flask application and a Postgres database. The Flask app uses python scripts like [legerible.py](Webapp\code\app\legerible.py) and [book.py](Webapp\code\app\book.py) to handle backend operations, like SQL Queries and fetching data via APIs. Meanwhile the database folder contains the [init.sql](Webapp\database\init.sql) script that populates the database pod with initial data. This data can then be viewed with the help of [views.py](Webapp\code\app\views.py).

</ul>

<br>


## Setup Instructions

👉 To start the application head on over to [k8s/README.md](k8s/README.md). 👈

There you will find instructions on how to install the necessary software stack and start the BigData Application afterwards.

>NOTE: You don't need to follow the setup for minikube and microk8s, you have to decide to use one of them. (minikube is our recommendtion)

To access the website in your browser after going through the steps in [k8s/README.md](k8s/README.md):

Open  **website**: http://127.0.0.1:5000/

Open **spark dashboard**: http://127.0.0.1:7077/

<br>

## Screencast Demonstaration

...