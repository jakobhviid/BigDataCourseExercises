# Lecture 02 - HFDS and different file formats

## GENERAL
WIP: Create and issue on github if you encountering errors




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

**Note**: A minimal HDFS cluster should also work with only 1 name node but for some reason it fails to start when using only 1 replica.

It might take a long time to create the ZooKeeper and HDFS clusters. This is because the images are relatively large (almost 3GB in total) and the upload speed of the Stackable image registry is relatively low. To see what is going on with a specific pod you can use the `kubectl describe` command.

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