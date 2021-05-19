## Starting the app on Kubernetes

1. You need [Minikube](https://kubernetes.io/de/docs/tasks/tools/install-minikube/) or [Microk8s](https://microk8s.io/docs) to host a kubernetes cluster on your local machine.


2. You will need to install [Skaffold](https://skaffold.dev/docs/install/) if you don't have it installed already.

3. **Start the application**

In the main directory of this repository run the following command:

```
skaffold dev
```

4. You need to activate the ingress addon on in Minikube/Microk8s:

If you use **Microk8s** use this in your terminal:

```
microk8s enable ingress
```

If you use **Minikube** use this in your terminal:

```
minikube addons enable ingress
```

5. Fetch the ingress port to access the application:

```
kubectl get ingress
```

This should give you the IP-Address that you can paste in your webbrowser to access the application.