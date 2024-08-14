# HDFS



`bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8`
`bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8`


We will be using Kubernetes operators and helm charts from [stackable.tech](stackable.tech) for creating the HDFS cluster.

The commands below are copied from their documentation and can be found here: [HDFS - getting started](https://docs.stackable.tech/home/stable/hdfs/getting_started/installation#_helm).

## Installation



```
kubectl apply -f persistent-volume-claims.yaml
kubectl apply -f configmap.yaml
kubectl apply -f services.yaml
kubectl apply -f datanodes.yaml
kubectl apply -f namenode.yaml
```


```
kubectl delete -f namenode.yaml
kubectl delete -f datanodes.yaml
kubectl delete -f services.yaml
kubectl delete -f configmap.yaml
kubectl delete -f persistent-volume-claims.yaml
```






We will add the helm chart repository from [stackable.tech](stackable.tech).

```
helm repo add stackable-stable https://repo.stackable.tech/repository/helm-stable/
```
And install the required Kubernetes operators for running an HDFS cluster.
```
helm install --wait zookeeper-operator stackable-stable/zookeeper-operator --version 23.7.0
helm install --wait hdfs-operator stackable-stable/hdfs-operator --version 23.7.0
helm install --wait commons-operator stackable-stable/commons-operator --version 23.7.0
helm install --wait secret-operator stackable-stable/secret-operator --version 23.7.0
```

Then we are ready to deploy HDFS and its required services.

### Set up an HDFS cluster 
The three yaml-files `zk.yaml`, `znode.yaml`, and `hdfs.yaml` have been taken directly from [Set up an HDFS cluster](https://docs.stackable.tech/home/stable/hdfs/getting_started/first_steps)


#### Setup Zookeeper
Apply the two yaml-files: `zk.yaml` and `znode.yaml`.
```
kubectl apply -f zk.yaml
kubectl apply -f znode.yaml
```
And wait for Zookeeper deployment to complete.

```
kubectl rollout status --watch --timeout=5m statefulset/simple-zk-server-default
```


#### Setup HDFS
Apply the single yaml-file: `hdfs.yaml`.
```
kubectl apply -f hdfs.yaml
```

And wait for HDFS deployment to complete.
```
kubectl rollout status --watch --timeout=5m statefulset/simple-hdfs-datanode-default
kubectl rollout status --watch --timeout=5m statefulset/simple-hdfs-namenode-default
kubectl rollout status --watch --timeout=5m statefulset/simple-hdfs-journalnode-default
```

### Verify HDFS works
Deploy a temporary helper pod `webhdfs.yaml` to interact with HDFS.
```
kubectl apply -f webhdfs.yaml
```
And wait for completion:
```
kubectl rollout status --watch --timeout=5m statefulset/webhdfs
```

We expect the HDFS cluster to be empty once installed. The following alias will used for accessing the content of the root directory in HDFS by the helper pod. 
```
alias hdfsls='kubectl exec webhdfs-0 -- curl -s -XGET "http://simple-hdfs-namenode-default-0:9870/webhdfs/v1/?op=LISTSTATUS"'

hdfsls

{
    "FileStatuses": {
        "FileStatus": [
        ]
    }
}
```

#### Add file to HDFS
1. Copy a file (`hdfs.yaml`) from localhost to `/tmp` of the helper pod. ```kubectl cp ./hdfs.yaml webhdfs-0:/tmp```
1. Put the file on HDFS. Start by getting the location:
    1. Extract the URL from ```kubectl exec webhdfs-0 -- curl -s -XPUT -T /tmp/hdfs.yaml "http://simple-hdfs-namenode-default-0:9870/webhdfs/v1/hdfs.yaml?user.name=stackable&op=CREATE&noredirect=true"``` it returns a location similar to: `"http://simple-hdfs-datanode-default-0.simple-hdfs-datanode-default.default.svc.cluster.local:9864/webhdfs/v1/hdfs.yaml?op=CREATE&user.name=stackable&namenoderpcaddress=simple-hdfs&createflag=&createparent=true&overwrite=false"`
    1. Insert the location ```kubectl exec webhdfs-0 -- curl -s -XPUT -T /tmp/hdfs.yaml "http://simple-hdfs-datanode-default-0.simple-hdfs-datanode-default.default.svc.cluster.local:9864/webhdfs/v1/hdfs.yaml?op=CREATE&user.name=stackable&namenoderpcaddress=simple-hdfs&createflag=&createparent=true&overwrite=false"```
1. Verify if the file `hdfs.yaml` is in HDFS: ```hdfsls```
1. Delete file and delete deployment of helper pod.
    1. Delete file: ```kubectl exec webhdfs-0 -- curl -s -XDELETE "http://simple-hdfs-namenode-default-0:9870/webhdfs/v1/hdfs.yaml?user.name=stackable&op=DELETE"``` -> ```{"boolean":true}```
    1. Delete helper pod: ```kubectl delete -f webhdfs.yaml ```