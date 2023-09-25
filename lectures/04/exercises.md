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

### Interacting with remote Kubernetes cluster

Retrieve the kubeconfig that is on the virtual machines. Then you can either merge it with your existing kubeconfig, which is recommended, or you can specify it using the `--kubeconfig` option.

If you merge the config, then simply copy the entries from the `clusters`, `users` and `contexts` lists to your kubeconfig file inside the `.kube` folder in your home directory.

Remember to tunnel port 16443. Use the following command: `ssh -NL 16443:127.0.0.1:16443 <name of node>`. Please note that you need to use `127.0.0.1` and not `localhost`.

## Port-forward service on remote Kubernetes cluster

The port-forward command might not work when you run it on your local machine (don't know why but it might have something to do with sdu firewall rules). To go around this we will have to tunnel a port on a virtual machine and run port-forward on the same virtual machine.

For example, if you want to connect to port 9001 on a service called `minio`, you want to do the following:

1. First SSH into the server and forward the desired port: `ssh -L 9001:127.0.0.1:9001 bds-g01-n01`. This will forward port `9001` on your machine to port `9001` on the remote machine named `bds-g01-n01`
2. Then use the port-forward command on the service: `microk8s kubectl port-forward svc/minio 9001:9001`. This will forward port `9001` on the virtual machine to port `9001` of the service called `minio`.

## Exercises

WIP 

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!

### Exercise 01 - Setup

Before you get to play around with Apache Spark you need to do some setup.

#### Stackable operators

You will need the commons, secret and spark-k8s Stackable operators. We will create them inside the `stackable` namespace.

**Task:** Install the Stackable operators

**Note:** MicroK8s uses a different kubelet directory than most other Kubernetes distributions. Specify the correct directory using `--set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet`.

<details>
  <summary><strong>Hint</strong>: Install operators</summary>

  Create the `stackable` namespace using `kubectl create namespace stackable`

  Then install the operators:

  ```text
  helm install -n stackable commons-operator stackable-stable/commons-operator --version 23.7.0
  helm install -n stackable secret-operator stackable-stable/secret-operator --version 23.7.0
  helm install -n stackable spark-k8s-operator stackable-stable/spark-k8s-operator --version 23.7.0
  ```
</details>

#### MinIO

Many of the tools on the Stackable platform integrates with S3 storage. We will primarily be using S3 to store historical data of Spark jobs that can then be viewed using a history server.

MinIO is an S3 compatible object store. It can be deployed using the [bitnami helm chart](https://github.com/bitnami/charts/tree/main/bitnami/minio/).

```text
helm install minio oci://registry-1.docker.io/bitnamicharts/minio --set service.type=NodePort --set defaultBuckets=spark-logs --set auth.rootUser=admin --set auth.rootPassword=password
```

**Note:** We set the user to `root` and password to `password` to ensure the username and password are the same. You could use other usernames and passwords but then you need to update the provided files.

MinIO Console is a web interface for MinIO. The port for the console is port `9001`.

**Tasks:** Log in to MinIO Console

**Hint:** [Port-forward service on remote Kubernetes cluster](#port-forward-service-on-remote-kubernetes-cluster)

#### Configurations

We will be using many different configurations. For the exercises it is not important to understand how it works but you can look at the comments in the file.

**Task**: Apply the [spark-configurations.yaml](./spark-configurations.yaml) file.

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