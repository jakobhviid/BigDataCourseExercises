# Services

## Install tools
```
kubectl
```

```
helm
```


## Common tricks in Kubernetes



### [Use Port Forwarding to Access Applications in a Cluster](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)

```
kubectl port-forward service/<name> <external>:<internal>
```
