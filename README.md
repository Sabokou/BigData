# BigData

The project "Legerible" for the module "Big Data" was designed by the following six group members:

- Alina Buss (4163246)
- Andreas
- Can
- Canberk
- Dominic Viola ()
- Phillip Lange (5920414)

The project resembles an online media library on the basis of a big data architecture with all necessary components.

<img src="Documentation\assets\Ziel-Architektur.jpg" >

## Table of Contents

---

1. [Use-Case](#Use-Case)
2. [Architecture and Design](#Architecture-and-Design)
3. [Folder Structure](#Folder-Structure)
4. [Setup Instructions](#Setup-Instructions)
5. [Screencast Demonstration](#Screencast-Demonstration)

---

<br>

## Use-Case

The media libary has the primary function of allowing user to loan books. This loan is given the idea more reflective of
a download functionality. To "loan" books one has to be logged in via the log-in functionality which is situated in the
top right corner of the page. There are three users created one of which being
"nadia" with password "1234". The navigation bar is situated on the left-hand side and can be used to navigate between
the different pages.

The first page - the homepage - provides an overview of the ten most loaned books, and the total amount of loans and
books in the system. The top ten is created as a result of the kafka messages send to the backend in Spark.

The second page - the "books page" - provides an overview of all books that are saved in the postgres database depending
on if the user is logged a "Loan" button is added to each row of the table. Furthermore, a button is provided to
simulate 50 books being loaned at random. Each loan is saved to the database directly and published via Kafka.
Additionally, a search function is provided to find books more easily.

The third page - the "profile" page - provides an overview of all user information like address, name and their loans.
Moreover, a user is presented with 4 recommendations based on previously loaned books, which are computed in the spark
backend with a cosine similarity.

The fourth page - the "loans" page - is an overview of all loans currently in the system.

<br>

## Architecture and Design

...

**Kubernetes architecture**

Kubernetes is the container management system that enables this distributed application.
Different microservices are created, automatically managed and connected to each other.
The following illustration shows which Kubernetes resources are used and how they relate to each other:

<br>
<img src="Documentation\assets\Kubernetes-structure.jpg" >
<br>
<br>

The dashed boxes on the right are distributed applications that are deployed with helm, a package manager for Kubernetes
resources. Cassandra is a distributed database management system that can scale and store data redundantly and is
therefore failure-resistent. Kafka is a software for message streaming and coordination, it is especially useful to
reduce communication overhead between different applications. Spark is used to analyse, enrich and manipulate the
streaming data.

The boxes on the left are kubernetes resources that we developed based on Docker images. The flask webapp to provide a
user with an interface for the fictional legerible library, display information and ingest user data into the system.
The postgresql database stores user and book related data, while the memcached cache servers provide users with a fast
retrieval time for consecutive requests for the same data.


<br>

## Folder Structure

<ul>

<li><b> Main folder </b></li>

In the main folder of this directory you can find skaffold.yaml. This file is used to create kubernetes artifacts which
are similar to containers, deploys helm charts and starts all kubernetes resources in the [k8s](k8s) folder. \
It also holds some resources that are used to build a container for the web app and a docker-compose.yml file that can
be used to run part of the infrastructure in docker instead of Kubernetes, this is just for debugging purposes.


<li><b> k8s </b></li>

The k8s folder holds Kubernetes resources like Services, LoadBalancer, Deployments and Pods. They are defined in YAML
files. \
Multiple specifications for the same software are written in the same YAML file separated by "---". This is helpful when
a deployment and a service reference the same pod.

You can read more about it [here](k8s/README.md).

<li><b> Kafka </b></li>

Kafka holds the resources for two pods: A *producer* and a *consumer*.\
The Producer streams randomly generated ISBN information into a Kafka topic, while the consumer reads from the same
topic and dumps the information to the console. The Kafka cluster is created via a helm chart, you can find the
specifics in [skaffold.yaml](skaffold.yaml).

For more information on Kafka resources look [here](Kafka/README.md)

<li><b> Spark </b></li>

The Spark folder contains resources to build a container that prepares dependencies and submits them together
with [spark-app.py](Spark/py-apps/spark-app.py) to the spark cluster, that is created [here](skaffold.yaml).

For more information on Spark click [here](Spark/README.md).

<li><b> Webapp </b></li>

The Webapp contains the resources for a Flask application and a Postgres database. The Flask app uses python scripts
like [legerible.py](Webapp\code\app\legerible.py) and [book.py](Webapp\code\app\book.py) to handle backend operations
like SQL queries and to fetch data via APIs. Meanwhile, the database folder contains
the [init.sql](Webapp\database\init.sql) script that populates the database pod with initial data. This data can then be
viewed with the help of [views.py](Webapp\code\app\views.py).

</ul>

<br>


## Setup Instructions

👉 To start the application head on over to [k8s/README.md](k8s/README.md). 👈

There you will find instructions on how to install the necessary software stack and start the BigData Application afterwards.

> NOTE: You don't need to follow the setup for minikube and microk8s, you have to decide to use one of them. (minikube is our recommendation)

To access the website in your browser after going through the steps in [k8s/README.md](k8s/README.md):

Open  **website**: http://127.0.0.1:5000/

Open **spark dashboard**: http://127.0.0.1:7077/

<br>

## Screencast Demonstration

...