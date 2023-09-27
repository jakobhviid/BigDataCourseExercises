# Lecture 04 - Spark

The exercises for this lecture are about Apache Spark. Apache Spark is a distributed computing framework for processing large datasets across clusters of computers. You will be deploying Apache Spark using the Stackable operators. 
You are expected to complete these exercises using the virtual machines made available to your semester project groups.

## Before you start

Before you start the exercises there are a few things you need to know to make it easier to work with the virtual machines and the Kubernetes cluster running on them.

Please note that you will be working on the same Kubernetes cluster as the rest of your group. We suggest that you use different namespaces while you work on the tasks, or just solve the exercises together. You should not be installing the Stackable operators multiple times, just install them once in the `stackable` namespace.

### Connect to virtual machines

Follow this [guide](https://www.youtube.com/watch?v=iKM6P7nRzqI) and verify that you can connect to your virtual machines using SSH. For example, to connect to `bds-g01-n0` (group 1 node 0) you would use the following command: `ssh bds-g01-n0`.


**Note:** [virtualresources.sdu.dk](https://virtualresources.sdu.dk).


**Note:** We recommend leaving the SSH session open during the exercise hours and running the `kubectl` commands from another terminal on your localhost to keep the same Kubernetes experience as in the previous lectures.

### Kubeconfig

The credentials used to connect to a Kubernetes cluster is stored in the kubeconfig file.
When you use minikube or Kubernetes with Docker Desktop then the kubeconfig file is automatically generated for you. The file is called `config` and is located in the `.kube` folder in your home directory.

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

- `clusters` is a list of Kubernetes clusters. It has the URI to the Kubernetes API and a certificate for the Kubernetes certificate authority.
- `users` is a list of users. It contains information used to authenticate the user.
- `contexts` is a list of contexts. A context associates a cluster and a user.

The name property for clusters, users and contexts can be anything. It is just a key to identify the cluster, context or user in the config file.

The `current-context` property is used to tell `kubectl` what context to use. It can be changed manually by modifying the file, or using kubectl: `kubectl config use-context <context name>`.

For further information, please look into [Organizing Cluster Access Using kubeconfig Files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) if you need to manage multiple Kubernetes environments.

### Retrieving kubeconfig from virtual machines

A MicroK8s cluster has been set up on the virtual machines. The kubeconfig for MicroK8s is located at `/var/snap/microk8s/current/credentials/client.config`. Connect to any of the virtual machines and copy the file to your localhost.

### Interacting with remote Kubernetes cluster

You can either merge the `config` file into your existing kubeconfig file, which is recommended, or you can specify a non-default `config` using the `--kubeconfig` argument in `kubectl`.

If you merge the `config` file, then simply copy the entries from the `clusters`, `users` and `contexts` lists to your kubeconfig file inside the `.kube` folder in your home directory.

**Note:** Please note that you need to use `127.0.0.1`.

## Exercises

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!

### Exercise 1 - Setup

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
  helm install -n stackable --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet secret-operator stackable-stable/secret-operator --version 23.7.0
  helm install -n stackable spark-k8s-operator stackable-stable/spark-k8s-operator --version 23.7.0
  ```
</details>

#### MinIO

Many of the tools on the Stackable platform integrates with S3 storage. We will primarily be using S3 to store historical data of Spark jobs that can then be viewed using a history server.

MinIO is an S3 compatible object store. It can be deployed using the [bitnami helm chart](https://github.com/bitnami/charts/tree/main/bitnami/minio/).

```text
helm install minio oci://registry-1.docker.io/bitnamicharts/minio --set service.type=NodePort --set defaultBuckets=spark-logs --set auth.rootUser=admin --set auth.rootPassword=password
```

**Note:** We set the user to `admin` and password to `password` to ensure the username and password are the same. You could use other usernames and passwords but then you need to update the provided files.

MinIO Console is a web interface for MinIO. The port for the console is port `9001`.

**Tasks:** Log in to MinIO Console

**Hint:** `kubectl port-forward svc/minio 9001:9001`

#### Configurations

We will be using many different Kubernetes configurations to manage the required resources. For these exercises, it is not important to understand how these resources work but you can look at the comments in the file.

**Task**: Apply the [spark-configurations.yaml](./spark-configurations.yaml) file.

### Exercise 2 - Running Spark jobs

Spark allows you to run programs on a cluster of machines. The "master" node is responsible for coordinating jobs running on the "worker" nodes.

Stackable Apache Spark is slightly different. Instead of having a cluster of Spark worker nodes ready at all times, a cluster is created for each job, and it will be teared down when the job is done. This allows you to get the best of both worlds of Apache Spark and Kubernetes - you get the data processing and reliability of Spark, and combine it with the abstractions, scalability, and tools that comes with Kubernetes. For example, you can automatically scale the amount of nodes in a Kubernetes cluster in the cloud using [cluster autoscalers](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler).

**Task:** Read about the [Stackable Operator for Apache Spark](https://docs.stackable.tech/home/stable/spark-k8s/index.html) and read the ["First steps" guide](https://docs.stackable.tech/home/stable/spark-k8s/getting_started/first_steps)

**Note:** You will get a better understanding of what you will be working with if you read it. So please read it.

Now that you have an idea of how the Stackable Operator works we will now take a look at the program for estimating pi that you just saw some examples with from the "First steps" guide.

**Task:** Inspect the [pi estimation program](https://github.com/apache/spark/blob/c1b12bd56429b98177e5405900a08dedc497e12d/examples/src/main/python/pi.py)

Try to visualize the [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) that this program will create. Take a look at [this](https://stackoverflow.com/a/30685279/9698208) to get a better idea of how Spark and DAGs.

You should now have some idea of what Spark programs looks like and how the pi estimation program works. You can also read a short explanation about it [here](https://spark.apache.org/examples.html).

A file containing a SparkApplication that will run the pi estimation program has been created for this exercise. It contains comments to better explain the different parts of it.

**Task:** Inspect the [02-spark-application.yaml](./02-spark-application.yaml) file

Before you apply the file you need to sign in to MinIO Console and upload any file to a folder called "eventlogs" in the "spark-logs" bucket or the Spark job will fail. The reason you need to upload a file to the folder is because you can't have empty folders in MinIO.

**Task:** Apply the [02-spark-application.yaml](./02-spark-application.yaml) file and then watch the pods being created using `kubectl get pods -w`

You should see a pod called `pyspark-pi-...` being created, shortly after that a pod called `pyspark-pi-...-driver` will be created. Shortly after that 3 pods called `pythonpi-...-exec-{1,2,3}` will be created. The exec pods will then finish, which is then followed by the driver becoming "Completed", and the `pyspark-pi` pod will also become "Completed".

Try to look at the logs of the the driver pod. There are a lot of things to look at, but look for the text `Pi is roughly...`. The result is only printed to the console, but you could modify the program to save it somewhere, such as HDFS, Kafka, or something else.

You should also notice that a file is uploaded to MinIO. This is a file that contains a lot of information about the job you just ran. The information can be viewed using a history server.

### Exercise 3 - History server

The Apache Spark History server is used to get information about [completed jobs](https://spark.apache.org/docs/latest/monitoring.html#viewing-after-the-fact). The logs of jobs will be stored in an S3 bucket, in our case the bucket called "spark-jobs" that was made with MinIO. The logs can be viewed using the history server.

We have not yet deployed the server. This can be done using the provided [spark-history-server.yaml](./spark-history-server.yaml) file.

**Task:** Apply the [spark-history-server.yaml](./spark-history-server.yaml) file.

Now that the history server is created then we want to access it.

**Task:** Access the history server.

**Hint:** `kubectl port-forward svc/spark-history-node 18080:18080`.

You should see a list of applications. You can click on the App ID to see more information about the applications.

You can see a visualization of the DAG by clicking on a completed job, or by going to "Stages", and then click on "DAG Visualization".

**Task:** How does the DAG visualization compare to what you thought it looked like?

### Exercise 3 - Analyzing files using Spark jobs

The previous program you ran was estimating pi. This program only used compute resources. But where Spark shines is with its data analysis capability.

In this exercise you will deploy a Spark job that will read a file and count the occurrences of different words in the file. You will be analyzing the alice in wonderland text from [lecture 2 exercise 4](../02/exercises.md#exercise-4---uploading-alice-in-wonderland-to-hdfs).

The file could be located in HDFS, but to simplify the exercise, we will just upload it to a new S3 bucket using MinIO.

**Task:** Create a new bucket called `spark-data`.

Now that you have created the bucket, then upload the file to the bucket using the "Object Browser".

**Task:** Upload alice in wonderland to the `spark-data` bucket.

Now that alice in wonderland is uploaded, you now want to take a look at the program you are about to run.

**Task:** Inspect the [word count program](https://github.com/apache/spark/blob/c1b12bd56429b98177e5405900a08dedc497e12d/examples/src/main/python/wordcount.py).

You can also read about the word count program from Apache Spark [here](https://spark.apache.org/examples.html).

The program counts the occurrences of all unique "words" in the input file. We will modify it to sort the result by the number of occurrences and to save the result back to S3 in different file formats. The file contains comments that help explain the code.

**Task:** Inspect the [customized word count program](./03-word-count.py).

Try to understand the different steps of the program.

A file containing a SparkApplication that will run the word count program has been created for this exercise. It contains comments to better explain the different parts of it.

**Tasks:** Inspect the [03-word-count-spark-application.yaml](./03-word-count-spark-application.yaml) file.

- Where is the main application file located?
- Where is the input file (alice in wonderland) located?
- How does Spark know how to connect to MinIO?

You should see that the SparkApplication has the main application file inside an S3 bucket called `spark-data`. Using S3 to store the program makes it easy to upload new programs. You don't need to build a new image every time you want to update your program!

**Task:** Upload the word count program to the `spark-data` bucket

**Task:** Apply the [03-word-count-spark-application.yaml](./03-word-count-spark-application.yaml) file and then watch the pods being created using `kubectl get pods -w`.

When the job is done then take a look at the logs of the driver pod and look for the word counts being printed. Also look inside the `spark-data` bucket to see the results. The results are stored in folders where there is a file that contains the data. Try downloading the files and see the results.

**Tasks:** Compare the size of the different results

- Which is the smallest?
- Which is the biggest?
- Why?

### Exercise 4 - Running Spark Streaming Jobs - Kafka
The objective of the exercise is to investigate the possibilities of using Spark streaming queries with a Kafka topic as a source. 

This exercise requires to have a Kafka producer which produces records for a topic. For convenience, we recommend revisiting [exercise 3](./../03/exercises.md#exercise-03---produce-messages-to-kafka-using-python) from the last lecture. 

**Task:** Create a streaming query that calculates the running mean of the six different stations. 

- You need to complete the query inside the [04-application.py](./04-application.py) file.
- Then opload the [04-application.py](./04-application.py) file to a bucket in MinIO. Similar to the previous exercise.
- Finally, apply the [04-application.yaml](./04-application.yaml) file using `kubectl apply -f ...`.


**Note**: There is no correct solution nor wrong solution for this exercise. You may find inspiration in the following links to complete the streaming query:
- [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#structured-streaming-programming-guide)
- [Operations on streaming DataFrames/Datasets](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#operations-on-streaming-dataframesdatasets)
- [Structured Streaming + Kafka Integration Guide ](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#structured-streaming-kafka-integration-guide-kafka-broker-versio)
