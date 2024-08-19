# HDFS

We will be using the following Docker images for the HDFS cluster:
- [bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8](https://hub.docker.com/r/bde2020/hadoop-namenode)
- [bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8](https://hub.docker.com/r/bde2020/hadoop-datanode)

## Installation
The following steps will guide you through the installation of an HDFS cluster on Kubernetes.
Before proceeding, make sure you have a Kubernetes cluster running and `kubectl` is configured to use the cluste and familiarize yourself with the following resoruce files:
- [configmap.yaml](./configmap.yaml)
- [datanodes.yaml](./datanodes.yaml)
- [namenode.yaml](./namenode.yaml)

Once ready, apply the following commands to deploy the HDFS cluster in the following order

1. Deploy the persistent volume claims.
````bash 
kubectl apply -f pvc.yaml
````

2. Deploy the configmap.
````bash 
kubectl apply -f configmap.yaml
````

3. Ensure it's deployed.

````bash
kubectl get configmap hadoop-config
````

4. Deploy the namenode.

````bash
kubectl apply -f namenode.yaml
````

5. Ensure the pod is created successfully

````bash
kubectl get pod -w
kubectl describe pod namenode-<ID>
kubectl logs namenode-<ID>
````

6. Deploy the datanodes.

````bash
kubectl apply -f datanodes.yaml
````

7. Ensure that 3 datanode pods are created 

````bash
kubectl get pod -w 
````

### Verify HDFS works
Create a connection to namenode pod using port-forwarding as below:

```bash
kubectl port-forward svc/namenode 9870:9870
```

We expect the HDFS cluster to be empty once installed. The following cmd will used for accessing the content of the root directory in HDFS by the namenode pod. 

```bash
curl -s -XGET "http://localhost:9870/webhdfs/v1/?op=LISTSTATUS"

{
    "FileStatuses": {
        "FileStatus": [

        ]
    }
}
```


## Cleanup

To remove the HDFS cluster, run the following commands:

1. Delete the datanodes and namenode pods
```bash
kubectl delete -f datanodes.yaml
kubectl delete -f namenode.yaml
```
2. Delete the configmap and persistent volume claims - if needed.
```bash
kubectl delete -f pvc.yaml
kubectl delete -f configmap.yaml
```