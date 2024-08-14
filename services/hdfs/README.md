# HDFS

We will be using the following Docker images for the HDFS cluster:
- `bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8`
- `bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8`

## Installation
The following steps will guide you through the installation of an HDFS cluster on Kubernetes.
Before proceeding, make sure you have a Kubernetes cluster running and `kubectl` is configured to use the cluste and familiarize yourself with the following resoruce files:
- [configmap.yaml](./configmap.yaml)
- [datanodes.yaml](./datanodes.yaml)
- [namenode.yaml](./namenode.yaml)

Once ready, apply the following commands to deploy the HDFS cluster.
```bash
kubectl apply -f configmap.yaml
kubectl apply -f datanodes.yaml
kubectl apply -f namenode.yaml
```

### Verify HDFS works
Create a connection to namenode pod using port-forwarding as below:

```bash
k8s port-forward svc/namenode 9870:9870
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

```bash
kubectl apply -f configmap.yaml
kubectl apply -f datanodes.yaml
kubectl apply -f namenode.yaml
```