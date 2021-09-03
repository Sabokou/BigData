# BigData

The project "Legerible" for the module "Big Data" was designed by the following six group members:

- Alina Buss (4163246)
- Andreas Dichter (6104795)
- Can Berkil (2087362)
- Canberk Alkan (3275561)
- Dominic Viola (1044258)
- Phillip Lange (5920414)

The project resembles an online media library on the basis of a big data architecture with all necessary components.

<img src="Documentation\assets\Ziel-Architektur.png" >

## Table of Contents

---

1. [Use-Case](#Use-Case)
2. [Architecture and Design](#Architecture-and-Design)
3. [Folder Structure](#Folder-Structure)
4. [Setup Instructions](#Setup-Instructions)
5. [Issues at the end](#Issues-at-the-end)
6. [Screencast Demonstration](#Screencast-Demonstration)
---

<br>

## Use-Case

The media library has the primary function of allowing users to loan books. These loans are more reflective of a
download functionality but since a true download functionality is out of scope for this project it was decided that it
would be considered as a loan instead. To "loan" books one has to be logged in via the log-in functionality which is
situated in the top right corner of the page. There are three users created one of which being
"nadia" with password "1234". The navigation bar is situated on the left-hand side and can be used to navigate between
the different pages.

The first page - the homepage - provides an overview of the ten most loaned books and the total amount of loans and
books in the system. The top ten are created as a result of the Kafka messages send to the backend in Spark.

The second page - the "books page" - provides an overview of all books that are saved in the Postgres database depending
on if the user is logged a "Loan" button is added to each row of the table. Furthermore, a button is provided to
simulate 50 books being loaned at random. Each loan is saved to the database directly and published via Kafka.
Additionally, a search function is provided to find books more easily.

The third page - the "profile" page - provides an overview of all user information like address, name, and their loans.
Moreover, a user is presented with 4 recommendations based on previously loaned books, which are computed in the spark
backend with cosine similarity.

The fourth page - the "loans" page - is an overview of all loans currently in the system.

<br>

## Architecture and Design

<img src="Documentation\assets\kappa-architecture.jpg" >

<br>
<br>
The chosen architecture for the big data application follows the **Kappa paradigm**. Data is streamed into the big data
processing system (in our case Spark) and processed as a stream (streaming is achieved with Kafka). The streaming data
is enriched by static data from the database to ensure that all relevant data is taken into consideration.

The streaming source a container streams random ISBNs from the Google books API into a Kafka topic. This simulates new
books that would be added to the legerible book platform.

The data stream is then ingested from Kafka by a consumer, added to the database of the library, and processed by Spark
to enhance book recommendations. The resulting data from spark processing are then dropped into the data lake, where it
can be used for business logic or analysis in the future. The data lake is implemented with Apache Cassandra, a
distributed database management system that supports scalability and is fault-tolerant due to replication.

New books are streamed into the system in small quantities, therefore, it is not necessary to form batches of data.
Thus, the Kappa architecture, where data is streamed into the system, is preferable in our use-case to using a Lambda
architecture in which data is first aggregated into batches.


<br>

**Kubernetes architecture**

Kubernetes is the container management system that enables this distributed application. Different microservices are
created, automatically managed and connected to each other. The following illustration shows which Kubernetes resources
are used and how they relate to each other:

<br>
<img src="Documentation\assets\Kubernetes-structure.jpg" >
<br>
<br>

The dashed boxes on the right are distributed applications that are deployed with helm, a package manager for Kubernetes
resources. Cassandra is a distributed database management system that can scale and store data redundantly and is
therefore failure-resistant. Kafka is a tool for message streaming and coordination, it is especially useful to reduce
communication overhead between different applications. Spark is used to analyze, enrich and manipulate the streaming
data.

The boxes on the left are Kubernetes resources that we developed based on Docker images. The flask web app provides a
user with an interface for the fictional legerible library, displays information, and ingests user data into the system.
The PostgreSQL database stores user and book related data, while the Memcached cache servers provide users with a fast
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
with [spark-app.py](Spark/Loan_Counts/py-apps/Spark_Loan_Counts.py) to the spark cluster, that is
created [here](skaffold.yaml). This however proved to not function due to limitations in the interaction between Spark's
standalone cluster and PySpark
being [incompatible] (https://github.com/bitnami/charts/issues/1626#issuecomment-571652789). It was then decided to use
local deployment instead to circumvent the problem. For more information on Spark click [here](Spark/README.md).

<li><b> Webapp </b></li>

The Webapp contains the resources for a Flask application and a Postgres database. The Flask app uses python scripts
like [legerible.py](Webapp/code/app/legerible.py) and [book.py](Webapp/code/app/book.py) to handle backend operations
like SQL queries and to fetch data via APIs. Meanwhile, the database folder contains
the [init.sql](Webapp/database/init.sql) script that populates the database pod with initial data. This data can then be
viewed with the help of [views.py](Webapp/code/app/views.py).

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

## Issues at the end

The entire project is not deployable on older hardware or laptops due to the unavailability of CPU cores and RAM. This
lead to the majority of participants being unable to test the entire project working at once and seeing if the
communication between individual components worked or not.

Trying to utilize a Spark standalone cluster instead of deploying to local introduced a multitude of problems towards
the end that resulted in a long troubleshooting process especially due to the nature of the error eluding us for a long
time given that the error was:

```WARN TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources```

This could easily have been in correlation to insufficient RAM or CPU cores for the container. Especially since the
primary answers found in the context is that the workers and or the job just needs to be allocated additional resources.
Additionally, we found out that the normal way of packaging python libraries and relying on the package installer of the
aforementioned cluster doesn't work and we figured out a workaround by using the **virtual environment** feature and
submitting the libraries as an archive instead of as python-files.

The used Kafka installation is also problematic as it takes longer than most containers to stabilize and properly
deploy. Leading to multiple crashes during startup and potentially during the stabilization phase, which results in the
skaffold not being deployed.

## Screencast Demonstration
If this embedding doesn't work, you can also view the video after downloading it [here](Documentation/assets/legerible_screencast_presentation.mkv).

Alternatively you can view the video with this link: https://youtu.be/JeYr-gIW1EA

<video src='./Documentation/assets/legerible_screencast_presentation.mkv' />