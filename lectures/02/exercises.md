# Lecture 02 - HFDS and different file formats

## GENERAL
WIP: Create and issue on github if you encountering errors


## Use VS Code to attach to a container in a Kubernetes cluster



## Subject and objective for these exercises

## Exercises

### Exercise 1 - Set up HDFS cluster

You will need a working HDFS cluster to solve the exercises for today. To set up HDFS, we will be using a [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) made by a company called [Stackable](https://stackable.tech/). Kubernetes operators are custom controllers that automate the management of applications within Kubernetes clusters and may make use of [custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/).

To keep the cluster tidy we will install the Stackable operators inside its own namespace. A namespace is a Kubernetes resource that can be used to better organize resources.

**Task**: Create a namespace called `stackable`.

To install the operators needed to set up the HDFS cluster you can follow their [installation guide using Helm](https://docs.stackable.tech/home/stable/hdfs/getting_started/installation#_helm). This is similar to the [exercise 6 from last week](../01/exercises.md#exercise-6---deploying-application-using-helm) where you installed the hello-kubernetes application using helm, except now install something using a helm repository.

**Task**: Install the nessesary Stackable operators to set up a HDFS cluster inside the `stackable` namespace. **Hint**: `helm install -n stackable ...`.

You can verify that the operators are installed by checking if there are 4 pods inside the stackable namespace, one for each operator you installed.

**Hint**: To get resources inside a specific namespace add `-n stackable` to the kubectl command, for example: `kubectl -n stackable get pods`.

Once all operator pods have the "Running" status, you can then proceed to create the HDFS cluster. You can follow the [Stackable guide to create a HDFS cluster](https://docs.stackable.tech/home/stable/hdfs/getting_started/first_steps). But before you can create the HDFS cluster you will need to create a ZooKeeper cluster. ZooKeeper is a centralized application for storing and syncronizes state and is used by HDFS for [failure detection and automatic failover](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithNFS.html#Automatic_Failover). ZooKeeper has a hierical data model where each node can have children nodes associated with it. Each node is called a ZNode. You can read more about how ZooKeeper stores data [here](https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#ch_zkDataModel).

**Note**: If you are using minikube and have multiple nodes you need to start the cluster using `minikube start --cni=flannel` for the next steps to work properly.

**Tasks**:

1. Create a ZooKeeper cluster with 1 replica
2. Create a ZNode for the HDFS cluster
3. Create a HDFS cluster with 2 name nodes, 1 journal node, and 1 data node

**Hint**: Follow the Stackable guide.

**Note**: For a highly available HDFS setup you will need a ZooKeeper cluster with atleast 3 nodes to maintain quorum, and a HDFS cluster made up of atleast 2 JournalNodes, 2 NameNodes, 2 DataNodes and a replica factor of 2. This might be excessive for a laptop so the exercises will assume a minimal setup.

**Note**: A minimal HDFS cluster should also work with only 1 name node but for some reason it does not with with the Stackable operator.

It might take a long time to create the ZooKeeper and HDFS clusters. This is because the images are relatively large (almost 3GB in total) and the upload speed of the Stackable image registry is relatively low. To see what is going on with a specific pod you can use the `kubectl describe` command.

### Exercise 2 - Interacting with HDFS cluster using CLI

Now that we have a HDFS cluster lets now try and use it. HDFS has a CLI tool for interacting with HDFS clusters. Because the cluster is running inside of Kubernetes, we also need to access it from inside Kubernetes.

Much like you created an interactive container with Ubuntu [last week](../01/exercises.md#exercise-7---interactive-container) you now need to create an interactive container using the `apache/hadoop:3` image.

**Task**: Create interactive container with the `apache/hadoop:3` image

HDFS works much like a normal file system. The commands to interact with HDFS are also similar to the commands you would use on a Unix system (such as Linux and Mac). For example, to list files and folders in a directory you would use the following command `hdfs dfs -ls /`.

**Tasks**:

1. Use the command `hdfs dfs -ls /`. What does it tell you?
2. Compare the output to `ls -laL /`

Because we have not configured the HDFS CLI tool to use the HDFS cluster it fails back to the local file system. The command `hdfs dfs -ls /` is actually equivilant to `ls -laL /`.

To use the HDFS cluster we need to tell the HDFS CLI to use the HDFS cluster we have made. This is done using the `-fs` option, for example: `hdfs dfs -fs hdfs://namenode:port`. You also need to use the "stackable" user when interacting with the HDFS cluster. This can be done by setting an environment variable for the current shell session: `export HADOOP_USER_NAME=stackable`.

**Task**: Try to list the files inside the root directory in the HDFS cluster

**Note**: Make sure you connect to the active name node. Only one name node is active, the other ones are in "standby" mode and will only be promoted in case of a failover. You know if it is not the active one if the result of the command is `Operation category READ is not supported in state standby`.

<details>
  <summary><strong>Hint</strong>: hostname and port</summary>

  The port that the HDFS client uses is 8020.

  There is a service called simple-hdfs-namenode-default with no ip. The service is a ["headless service"](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services). This means that the service does not provide load balancing and proxying, but it does provide DNS resolution for pods that match the selector: `pod-name.service-name` will return the IP of the pod.
</details>

<details>
  <summary><strong>Hint</strong>: Full example</summary>

  The service called "simple-hdfs-namenode-default" is a ["headless service"](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services). 

  Use `kubectl get pods` to get a list of all pods. If you have two name nodes then the pods should be called "simple-hdfs-namenode-default-0" and "simple-hdfs-namenode-default-1". To get the IP of the pod running name node 0, tha would be the following domain `simple-hdfs-namenode-default-0.simple-hdfs-namenode-default`. You can choose either one of the pods but it may not be the active one. If it is not the active one then try a different name node. The port for HDFS NameNode metadata service is 8020, which is what HDFS clients use.

  Before we run a command inside the interactive container we need to set the HDFS username: `export HADOOP_USER_NAME=stackable`.

  The full command would for example be `hdfs dfs -fs hdfs://simple-hdfs-namenode-default-0.simple-hdfs-namenode-default:8020 -ls /` for name node 0.
</details>

You should see that there are no files in the directory. We will fix this now.

**Task**: Create a file inside the interactive container called "test.txt" and add some text to it.

<details>
  <summary><strong>Hint</strong>: Creating a file</summary>

  The container does not have nano or vim installed. You can simply create a file by echoing some text and piping it into a file: `echo "hello" > test.txt`. Verify that the file exists by using `ls` and verify its contents using `cat test.txt`.
</details>

To add a file to the HDFS cluster using the HDFS CLI you can use the put command.

**Task**: Upload the file to the HDFS cluster

<details>
  <summary><strong>Hint</strong>: Uploading the file</summary>

  `hdfs dfs -put ./test.txt /test.txt`
</details>

Now that you have uploaded a file to HDFS you can try to list the files to verify that it is added. Similarly to Unix systems you can use the `cat` command to read files.

**Task**: Read the contents of the file you just uploaded to HDFS

<details>
  <summary><strong>Hint</strong>: Reading the file</summary>

  `hdfs dfs -cat /test.txt`
</details>

**Task**: Try to delete the file from HDFS

**Hint**: Run the command `hdfs dfs` to get a list of all commands and options.

<details>
  <summary><strong>Hint</strong>: Deleting the file</summary>

  `hdfs dfs -rm /test.txt`
</details>

You are now able to list files and folders, read files, upload files, and delete files, using HDFS.

### Exercise 3 (optional) - Mount HDFS config to interactive container

Instead of manually specifying the uri ("hdfs://namenode:port") and making sure you connect to the correct name node you can let the HDFS client decide this for you using a HDFS config file(s) (called "core-site.xml" and "hdfs-site.xml").

The Stackable operator creates a Kubernetes resource called a ConfigMap. A ConfigMap is a resource that contains key-value pairs used for configuration. It can be used in various ways, but we want to mount the ConfigMap as a file to the interactive container.

Before we mount it we want to take a look at the ConfigMap and try to understand it.

**Task**: Get the contents of the ConfigMap resource using the `kubectl describe` command.

**Hint**: The ConfigMap resource should be called "simple-hdfs".

<details>
  <summary><strong>Hint</strong>: Full example</summary>

  List all ConfigMaps using `kubectl get configmap`.

  There should be a ConfigMap called "simple-hdfs".

  Describe the ConfigMap using `kubectl describe configmap/simple-hdfs`.
</details>

To create the interactive container and mount the config, use the provided [hdfs-cli.yaml file](./hdfs-cli.yaml)

### Exercise 4 - Attach vscode to pod

If you install the Kubernetes extension for Visual Studio Code then you can connect to the container using vscode. This will allow you to run commands and create files using vscode, but inside the container. You can read about it [here](https://code.visualstudio.com/docs/devcontainers/attach-container#_attach-to-a-container-in-a-kubernetes-cluster).

Simply install the extension and click on the Kubernetes icon in the primary side bar. Then select the cluster you want to use, click on workloads, pods, and then right.click the pod you want to attach to and then click "Attach Visual Studio Code". This will open a new vscode window that is connected to the pod.

### Exercise 3 - Access txt data on HDFS from a Python client (Read and write)

Now we want to access HDFS from a client. To do this we will create a Python client that can read and write to HDFS.

TODO: Interactive session
complete `simple-client.py`


### Exercise 4 - Create JSON data to HDFS from a Python client


Now that we have a python client that can write from HDFS. We can try to write JSON from HDFS.
TODO: Interactive session
complete `counting-json.py`

Questions:
- What are the five most common words in TODO?? Alice in Wonderland, and how many times are they repeated?

### Exercise 5 - Create avro data to HDFS from a Python client


Now that we have a python client that can write from HDFS. we can try to write JSON from HDFS.
TODO: Interactive session
complete `counting-avro.py`

Questions:
- What are the five least common words in TODO?? Alice in Wonderland, and how many times are they repeated?

### Exercise 6 - Create parquet data to HDFS from a Python client


Now that we have a python client that can write from HDFS. we can try to write JSON from HDFS.
TODO: Interactive session
complete `counting-parquet.py`

Questions:
- What is the schema??
- Hvordan vil tabellen se ud med i bred format?


### Exercise 7 - Create six fictive data sources

Simulate multiple data streams from an identical sensor with a sample frequency of 1hz placed a six different locations. 

- You need to find a proper directory pattern to store these samples in HDFS for later analysis
- Which file format do we prefer?
- The schema of a sample may be similar to:
```json

{
    "payload": {
        "station_id": "1", // value in <"1", "2", "2", "3", "4", "5">
        "modality": 11.0, // value between 0 and 600
        "unit": "MW", // unit
        "temporal_aspect":"real_time", // value in <"real_time", "edge_prediction">
    },
    "correlation_id": "23c4d380-b357-4082-9298-314ba9ef1b68", // correlation uuid for this sample
    "created_at": 1667205100.786588, // UNIX time
    "schema_version": 1
}
```
- write a data producer for simulating these six sensors and use of the python client logic to write files into HDFS


Questions:
- What is the schema??
- What is the proper folder structure inside HDFS?
- 