# Lecture 07 - Metadata, Data Provenance and Data Mesh

## Exercises

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!

Before you start working on the exercises you are strongly encouraged to clean up your Kubernetes cluster. The exercises will assume you use the MicroK8s cluster on the provided virtual machines and that the cluster is in a "clean" state.

### Exercise 1 - 

[Deploying DataHub with Kubernetes](https://datahubproject.io/docs/deploy/kubernetes/)

```
k8s create namespace meta
```

```
kubectl -n meta create secret generic mysql-secrets --from-literal=mysql-root-password=datahub
kubectl -n meta create secret generic neo4j-secrets --from-literal=neo4j-password=datahub
```

```
helm repo add datahub https://helm.datahubproject.io/
```

```
helm install -n meta prerequisites datahub/datahub-prerequisites --values lectures/07/values.yaml
```

```
kubectl get pods -n meta -w  
```

```
helm install -n meta datahub datahub/datahub
```

```
kubectl get pods -n meta -w  
```

```
kubectl port-forward <datahub-frontend pod name> 9002:9002
```