# Lecture 04 - Spark

The exercises for this lecture are about Apache Spark. Apache Spark is a unified analytics engine for big data processing, with built-in modules for streaming, SQL, machine learning, and graph processing. It can be used to process large amounts of data in parallel on a cluster of computers.
Apache Spark is built to work on top of the Hadoop ecosystem and can be used to process data stored in HDFS, S3, or other storage systems. Spark can be used to process data in batch or in real-time using Spark Streaming.

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!





## Exercises

### Exercise 1 - Setup

Before you get to play around with Apache Spark you need to do some setup.

```bash
helm install spark oci://registry-1.docker.io/bitnamicharts/spark
```

### Exercise 2 - Running a Spark job locally and in your deployment

The first exercise is to run a Spark job that estimates pi. The program is written in Python and is located in the Spark repository. The program is an example of how to run a Spark job. The program is simple and only uses compute resources.

**Task**: Inspect the [pi-estimation.py](./pi-estimation.py) file.

**Task**: Try to visualize the [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) this program will create. 
**Help**: 
- Take a look [here](https://stackoverflow.com/a/30685279/9698208) to better understand how the DAG is created for the Spark program.
- You are able to get other examples of Spark programs [here](https://spark.apache.org/examples.html).

**Task**: Run the [pi-estimation.py](./pi-estimation.py) file locally.
- How will the number of partitions affect the result?

**Task**: Update the [pi-estimation.py](./pi-estimation.py) file to be executed on the inside your Kubernetes cluster.
- Does the number of partitions affect the runtime? 
- How does the runtime compare to running the program locally?


### Exercise 3 - Analyzing files using Spark jobs

The previous program you ran was estimating pi. This program only used compute resources. But where Spark shines is with its distributed data analysis capability.

In this exercise you will run a Spark job that will read a file and count the occurrences of different words in the file. You will be analyzing the alice in wonderland text from [lecture 2 exercise 3](../02/exercises.md#exercise-3---uploading-alice-in-wonderland-to-hdfs).

**Task**: Ensure the [alice in wonderland](https://www.gutenberg.org/files/11/11-0.txt) file is within your HDFS cluster. If not upload the file to HDFS.

**Task**: Inspect the [word-count.py](./word-count.py). The program counts the occurrences of all unique "words" in the input file.
- Try to run the program locally and in the cluster pointing towards different input files.

**Notice**:You can also read about the word count program from Apache Spark [here](https://spark.apache.org/examples.html) and [here](https://github.com/apache/spark/blob/c1b12bd56429b98177e5405900a08dedc497e12d/examples/src/main/python/wordcount.py).


### Exercise 4 - Running Spark Streaming Jobs - Kafka
The objectives of this exercise are to run a Spark streaming job that reads from a Kafka topic.
This exercise requires to have a Kafka producer which produces records for a topic. For convenience, we recommend revisiting [exercise 3](./../03/exercises.md#exercise-3---produce-messages-to-kafka-using-python) from the last lecture. TODO: ANBAE validate this link is correct.

**Task**: Create a streaming query that calculates the running mean of the six different stations produced to the Kafka topic called `INGESTION`.

**Help**: You need to complete the query inside the [process-streaming.py](process-streaming.py) file.


**Important note**: There is no correct solution nor wrong solution for this exercise. You may find inspiration in the following links to complete the streaming query:
- [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#structured-streaming-programming-guide)
- [Operations on streaming DataFrames/Datasets](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#operations-on-streaming-dataframesdatasets)
- [Structured Streaming + Kafka Integration Guide ](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#structured-streaming-kafka-integration-guide-kafka-broker-versio)
