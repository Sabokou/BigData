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


## 2. Install skaffold
You will need to install [Skaffold](https://skaffold.dev/docs/install/) if you don't have it installed already.

## 3. Activate Ingress addon

You need to activate the ingress addon on in Minikube/Microk8s:

If you use **Microk8s** use this in your terminal:

```
microk8s.enable dns ingress
```

If you use **Minikube** use this in your terminal:

```
minikube addons enable ingress
```

## 4. Start the application

In the main directory of this repository run the following command:

```
skaffold dev
```

## 5. Access the application

There are two different ways to access the application. On Linux and MacOS it can be accessed via ingress. On Windows on the other hand it is for some reason not possible to access the ingress, therefore we will access it via LoadBalancer.

### **5.1. Only Linux and MacOS:**
Fetch the ingress port to access the application:

```
kubectl get ingress
```

This should give you the IP-Address that you can paste in your webbrowser to access the application.

### **5.2 Only Windows**

Using minikube to make the loadbalancer accessable from http://localhost:5000:

```
minikube tunnel
```

Using microk8s to make the loadbalancer accessable: Not tested yet.


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