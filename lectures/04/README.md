# Lecture 04 - Spark

The exercises for this lecture are about Apache Spark. Apache Spark is a unified analytics engine for big data processing, with built-in modules for streaming, SQL, machine learning, and graph processing. It can be used to process large amounts of data in parallel on a cluster of computers.
Apache Spark is built to work on top of the Hadoop ecosystem and can be used to process data stored in HDFS, S3, or other storage systems.

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!

## Exercises

### Exercise 1 - Deploying Apache Spark on Kubernetes

Before you get to play around with Apache Spark you need to deploy your Spark environment on your Kubernetes cluster. We will be using a helm chart to deploy Spark on Kubernetes.

**Task**: Inspect the [spark-values.yaml](./spark-values.yaml) file to see how the Spark deployment is configured.

**Task**: Install the Spark Helm chart using the following command:

```bash
helm install --values spark-values.yaml spark oci://registry-1.docker.io/bitnamicharts/spark --version 9.2.9
```

**Task**: Inspect the UI of the Spark deployment and validate that there are two worker nodes alive.

```bash
kubectl port-forward svc/spark-master-svc 8080:80
```

### Exercise 2 - Running a Spark job locally and in your deployment

The first exercise is to run a Spark job that estimates pi. The program is written in Python and is an example of how to create a Spark job that both can run on your localhost and in your Spark environment.

**Task**: Inspect the [pi-estimation.py](./pi-estimation.py) file.

**Task**: Try to visualize the [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) this program will create.

**Help**:

- Take a look [here](https://stackoverflow.com/a/30685279/9698208) to better understand how the DAG is created for the Spark program.
- You are able to get other examples of Spark programs [here](https://spark.apache.org/examples.html).

**Task**: Run the [pi-estimation.py](./pi-estimation.py) file locally using Python 3.12.

- How will the number of partitions argument affect the result?

**Task**: Update the [pi-estimation.py](./pi-estimation.py) file to be executed on the inside your Kubernetes cluster.

- Does the number of partitions affect the runtime?
- How does the runtime compare to running the program locally?

### Exercise 3 - Analyzing files using Spark jobs

The previous program you ran was estimating pi. This program only used compute resources and in this exercise you will run a Spark job that will read a file and count the occurrences of different words in the file. You will be analyzing the alice in wonderland text from [lecture 2 exercise 3](../02/README.md#exercise-3---uploading-alice-in-wonderland-to-hdfs).

**Task**: Ensure the [alice in wonderland](https://www.gutenberg.org/files/11/11-0.txt) file is within your HDFS cluster. If not upload the file to HDFS.

**Task**: Inspect the [word-count.py](./word-count.py). The program counts the occurrences of all unique "words" in the input file.

- Try to run the program locally and in the cluster pointing towards different input files.

**Notice**:You can read about the word count program from Apache Spark [here](https://spark.apache.org/examples.html) and [here](https://github.com/apache/spark/blob/c1b12bd56429b98177e5405900a08dedc497e12d/examples/src/main/python/wordcount.py).

### Exercise 4 - Average sample values from JSON files stored in HDFS

Let us assume that you have a dataset of sample records stored in HDFS. The dataset is stored in JSON format and contains defined by the [exercise 9 from lecture 02](../02/README.md#exercise-9---create-six-fictive-data-sources).

In this exercise you will run a Spark job that will read all the JSON files and computes the average value of the `payload.modality` field for each station.

**Task**: Inspect the [avg-modalities.py](./avg-modalities.py).

**Task**: Ensure you have records stored in HDFS on the proper location. If not upload the records to HDFS.
**Task**: Run the your Spark application on the cluster. What is the `payload.modality` average value for each station?

### Exercise 5 - Running Spark Streaming Jobs - Kafka

The objective of this exercise is to create a Spark streaming job that reads from a Kafka topic. This exercise requires to have a Kafka producer which produces records in the a given topic. For convenience, we recommend revisiting the [exercise 4 from lecture 03](./../03/README.md#exercise-4---produce-messages-to-kafka-using-python).

**Task**: Create a streaming query that calculates the running mean of the six different stations (`payload.sensor_id`) produced to the Kafka topic `INGESTION`.

**Help**: You need to complete the query inside the [process-streaming.py](process-streaming.py) file.
**Notice**: You need to append additional packages as arguments to run the Spark streaming application to read from kafka. You can enable an interactive Spark streaming promt using `pyspark` or submitting your final Spark application using `spark-submit` as demonstrated below:

```bash
pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2
```

```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2 process-streaming.py
```

**Task**: Run your Spark streaming application and validate that the running means of `payload.modality` field is close to the calculated values in [exercise 4](README.md#exercise-4---average-sample-values-from-json-files-stored-in-hdfs).

**Important note**: There is no correct solution for this exercise. You may find inspiration in the following links to complete the streaming query:

- [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#structured-streaming-programming-guide)
- [Operations on streaming DataFrames/Datasets](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#operations-on-streaming-dataframesdatasets)
- [Structured Streaming + Kafka Integration Guide](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#structured-streaming-kafka-integration-guide-kafka-broker-versio)