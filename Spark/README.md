# Developer instructions to run Spark

## 1. Update Skaffold and Helm
You need the latest version of [Skaffold](https://skaffold.dev/docs/install/) and [helm](https://helm.sh/docs/intro/install/) to start the whole application with [Minikube](https://kubernetes.io/de/docs/tasks/tools/install-minikube/).
How you can update skaffold and helm depends on your package manager. 

On Windows for example (using [chocolatey](https://chocolatey.org/install))you would run:
```
choco upgrade skaffold
```

```Helm version``` should be 3.5.2 or later and ```skaffold version``` at 1.26.0 or later.

## 2. Add the bitnami repository
You add the bitnami repository to helm with this command:

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```
## 3. Start the application 

As described in the [Kubernetes README](../k8s/README.md) use the command ```skaffold dev``` to start all containers in
Kubernetes. Skaffold will deploy a spark cluster and a container that starts the spark app
at [./py-apps/spark-app.py](Loan_Counts/py-apps/Spark_Loan_Counts.py). The container downloads and packages all
necessary dependencies for the application, that are definined in [requirements.txt](Loan_Counts/requirements.txt).

Lastly if the spark job is started skaffold will also make a web GUI available to see the running jobs
at http://localhost:7077.


# Structure

Since there are two different applications using Spark for data processing a folder was created for each of them. Within
the following structure was used:
<ol>
<li> py-apps folder:</li>

Contains a python file that contains the logic for the spark job. The naming is specific, because a container will look
for these specific files.

<li> requirements.txt: </li>

Contains the dependencies, that are needed to run the spark job.

<li> Dockerfile </li>

Packages the dependencies and starts the spark job with the "spark-submit" script that comes with spark.
</ol>


# Troubleshooting notes
## Start a spark application manually

Now you can start the application for reference [here](../k8s/README.md) is the instruction how to start the application
on Kubernetes with minikube.

Important to note is that on startup, after the spark resources are created instructions are printed on how to submit a
demo application.

<details>
  <summary markdown="span">Startup instructions</summary>
  
  1. Get the Spark master WebUI URL by running these commands:

  kubectl port-forward --namespace legerible-spark svc/spark-release-master-svc 80:80
  echo "Visit http://127.0.0.1:80 to use your application"

2. Submit an application to the cluster:

To submit an application to the cluster the spark-submit script must be used. That script can be obtained
at https://github.com/apache/spark/tree/master/bin. Also, you can use kubectl run.

export EXAMPLE_JAR=$(kubectl exec -ti --namespace legerible-spark spark-release-worker-0 -- find examples/jars/ -name '
spark-example*\.jar' | tr -d '\r')

  kubectl exec -ti --namespace legerible-spark spark-release-worker-0 -- spark-submit --master spark://spark-release-master-svc:7077 \
    --class org.apache.spark.examples.SparkPi \
    $EXAMPLE_JAR 5
</details>


Here is a list of further readings for this topic:

- [Running Spark on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html#submitting-applications-to-kubernetes)
- [Overview what happens behind the scenes](https://www.datamechanics.co/blog-post/setting-up-managing-monitoring-spark-on-kubernetes)
- [Running Spark Jobs](https://databricks.com/de/session_na20/running-apache-spark-jobs-using-kubernetes)
- [Problems running PySpark on standalone clusters](https://github.com/bitnami/charts/issues/1626#issuecomment-571652789)

