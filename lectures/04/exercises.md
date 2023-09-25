# Lecture 04 - Spark

The exercises for this lecture is about Apache Spark. Apache Spark is a distributed computing framework for processing large datasets accross clusters of computers. You will be using Apache Spark using Stackable. You are expected to complete these exercises using the virtual machines made available to your semester project groups.

## Before you start

Before you start the exercises there are a few things you need to know to make it easier to work with the virtual machines and the Kubernetes cluster running on them.

### Connect to virtual machines

Follow this [guide](https://www.youtube.com/watch?v=iKM6P7nRzqI) and verify that you can connect to your virtual machines using ssh. For example, to connect to `bds-g01-n0` (group 1 node 0) you would use the following command: `ssh bds-g01-n0`.

### Tunnelling ports

To access ports on the virtual machines you need to use [SSH tunnelling](https://unix.stackexchange.com/a/115906).

When connecting you can also tunnel ports. For example, if you want to tunnel port 16443 on your local machine to port 16443 on the virtual machine you could use the following command: `ssh -L 16443:127.0.0.1:16443 bds-g01-n0`. If you want multiple ports you can add multiple `-L` options, for example: `ssh -L 16443:127.0.0.1:16443 -L 1234:127.0.0.1:1234 bds-g01-n0`. If you don't need a shell but simply needs to forward the ports then you can use `-NL` instead: `ssh -NL 16443:127.0.0.1:16443 bds-g01-n0`.

### Kubeconfig

Information to connect to a Kubernetes cluster is stored in kubeconfig files. When you use minikube or Kubernetes with Docker Desktop then the kubeconfig file is automatically generated for you. The file is called `config` and is located in the `.kube` folder in your home directory.

By default, `kubectl` looks for a file called `config` inside the the `.kube` folder in your home directory. To use a different kubeconfig file you can use `kubectl --kubeconfig <path to config>`.

A kubeconfig file may look like this:

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://127.0.0.1:16443
  name: microk8s-cluster
contexts:
- context:
    cluster: microk8s-cluster
    user: admin
  name: microk8s
current-context: microk8s
kind: Config
preferences: {}
users:
- name: admin
  user:
    token: REDACTED
```

The config contains three lists: `clusters`, `users` and `contexts`:

- `clusters` is a list of Kubernetes clusters. It has the uri to connect to the Kubernetes API and a certificate for the Kubernetes certificate authority.
- `users` is a list of users. It contains information used to authenticate the user.
- `contexts` is a list of contexts. A context associates a cluster and a user.

The name property for clusters, users and contexts can be anything. It is just a key to identify the cluster, context or user in the config file.

The `current-context` property is used to tell kubectl what context to use. It can be changed manually by modifying the file, or using kubectl: `kubectl config use-context <context name>`.

### Retrieving kubeconfig from virtual machines

A MicroK8s cluster has been set up on the virtual machines. The kubeconfig for MicroK8s is located at `/var/snap/microk8s/current/credentials/client.config`. Connect to any of the virtual machines and copy the file to your computer.

### Connecting to remote Kubernetes cluster

Retrieve the kubeconfig that is on the virtual machines. Then you can either merge it with your existing kubeconfig, which is recommended, or you can specify it using the `--kubeconfig` option.

If you merge the config, then simply copy the entries from the `clusters`, `users` and `contexts` lists to your kubeconfig file inside the `.kube` folder in your home directory.

## Exercises

WIP 

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!


### Exercise 01 - Composing a Spark Cluster


```sh
//  helm install -n stackable --wait commons-operator stackable-stable/commons-operator --version 23.7.0
// helm install -n stackable --wait secret-operator stackable-stable/secret-operator --version 23.7.0
helm install -n stackable --wait spark-k8s-operator stackable-stable/spark-k8s-operator --version 23.7.0
```

### Exercise 02 - Interacting with Spark
- Master: http://localhost:8080
- Quick demonstration of using Spark’s web UI.
    - Worker 1: http://localhost:8081 Worker 2: http://localhost:8082
    - Visualizes running Spark Jobs, resource usage, and the state of jobs

### Exercise 03 - Running a Local Spark Job
### Exercise 04 - Running a Spark Job in Kubernetes

### Exercise 04 - Spark Structured Streaming



#### Exercise 04.1 - HDFS as Source and Kafka as Sink

 Running a Spark Job in Kubernetes
Creating a HDFS directory
Let’s create a folder that can be used as a data ingestion source!
1. With the CLI:
1. docker exec -ti namenode bash
2. hdfs dfs -mkdir /stream-in - Creates a directory in HDFS called stream-in
2. With the Hadoop UI
1. Go to http://localhost:9870
2. Go to Utilities > Browse the file system > Create a directory

#### Exercise 04.2 - HDFS as Sink and Kafka as Source

 Running a Spark Job in Kubernetes
Creating a HDFS directory
Let’s create a folder that can be used as a data ingestion source!
1. With the CLI:
1. docker exec -ti namenode bash
2. hdfs dfs -mkdir /stream-in - Creates a directory in HDFS called stream-in
2. With the Hadoop UI
1. Go to http://localhost:9870
2. Go to Utilities > Browse the file system > Create a directory


### Exercise 05 - Clean Up