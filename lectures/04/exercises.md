# Lecture 04 - Spark


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