# Starting the app on Kubernetes

## 1. Install Kubernetes
You need [Minikube](https://kubernetes.io/de/docs/tasks/tools/install-minikube/) **or** [Microk8s](https://microk8s.io/docs) to host a kubernetes cluster on your local machine.

Before doing the following steps start the kubernetes cluster by running:

If you use Minikube:
```
minikube start
```

If you use Microk8s:
```
microk8s start
```

## 2. Activate Ingress addon

You need to activate the ingress addon on in Minikube/Microk8s:

If you use **Microk8s** use this in your terminal:

```
microk8s.enable dns ingress
```

If you use **Minikube** use this in your terminal:

```
minikube addons enable ingress
```

## 3. Install skaffold
You will need to install [Skaffold](https://skaffold.dev/docs/install/) if you don't have it installed already.

## 4. Install helm 

Next up you need helm, which functions like a package manager for kubernetes, we will use it to handle some parts of our application (kafka cluster creation).

Install [helm](https://helm.sh/docs/intro/install/) with you favorite package manager (e.g. [chocolatey](https://chocolatey.org/install) on Windows or [brew](https://docs.brew.sh/Installation) on MacOS, Linux distributions usually ship with a package manager)

Now follow the instructions on the [official helm website](https://helm.sh/docs/intro/install/) to install helm with your package manager.

## 5. Add Bitnami repository to helm
The bitnami repository will be used by helm to create a kafka cluster.

Run this in the terminal:

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```


## 6. Start the application

In the main directory of this repository run the following command:

```
skaffold dev
```

## 7. Access the application

There are two different ways to access the application. On Linux and MacOS it can be accessed via ingress. On Windows on the other hand it is for some reason not possible to access the ingress, therefore we will access it via LoadBalancer.

### **7.1. Only Linux and MacOS:**
Open a new terminal and fetch the ingress port to access the application:

```
kubectl get ingress/legerible-ingress
```

This should give you the IP-Address that you can paste in your webbrowser to access the application.

### **7.2 Only Windows**

Open a new terminal and use **minikube** to make the loadbalancer accessable from http://localhost:5000:

```
minikube tunnel
```

Using **microk8s** to make the loadbalancer accessable: Not tested yet.


# Tips for trouble shooting
1. Make sure that docker can be used on the command line. If not start the docker daemon
2. Make sure that a Kubernetes cluster is up and running (with minikube or microk8s)
3. If the Kubernetes resources were not deleted properly you can use
```
skaffold delete
```
to delete all Kubernetes ressources in this project and rebuild the project with 
```
skaffold dev
```
4. Skaffold might throw an error if there is an ingress that also listens to the prefix "/". You can solve this by running:
```
kubectl delete ingress/<ingress-name-you-want-to-delete>
```
5. It might be, that the default memory of the minikube kubernetes cluster (about 2GB) is insufficient. If you encounter problems with the ingress addon or the kafka cluster you can manually allocate more memory to minikube. This might help ```minikube stop & minikube start --cpu 2 --memory 4096```