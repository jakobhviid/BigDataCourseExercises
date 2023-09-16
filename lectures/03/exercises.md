# Lecture 03 - Distributed Transport and Streaming


## Exercises

The exercises for this week's lecture will be about distributed transport and streaming. You will be creating a Kafka cluster and various publishing programs and subscribing programs for streams of records.
The focus of today's lecture is to interact with Kafka, create Python producer and consumer programs, and configure Kafka connect modules. 

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!


### Exercise 01 - Composing a Kafka cluster

The objective of this exercise is to deploy a Kafka cluster. We will be using operators from a company called [strimzi.io](strimzi.io). The image below links to a short introductory video on how to set up Kafka inside Kubernetes. 

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/1qO2qGuJNQI/0.jpg)](https://www.youtube.com/watch?v=1qO2qGuJNQI)

For the remaining steps of this exercise copy and paste into the terminal and for those of you who need further descriptions continue reading here: [strimzi.io/quickstarts](https://strimzi.io/quickstarts/).

**NB:** Make sure you have the Kubernetes cluster running locally and start reading from the section "Deploy Strimzi using installation files" in the above-mentioned [link](https://strimzi.io/quickstarts/).


#### Essential files

We have chosen to fetch the manifest file to remove an external dependency. Therefore we recommend you familiarize yourself with the three mentioned files: 

- [strimzi-cluster-operator.yaml](./strimzi-cluster-operator.yaml)
- [kafka.yaml](./kafka.yaml)
- [kafka-extra.yaml](kafka-extra.yaml)

**NB:** Make sure your terminal path is relative to these files before moving forward.

#### Deploy Strimzi

**Task:** Create namespace `kafka` in Kubernetes.
<details>
  <summary><strong>Hint</strong>: Create Kubernetes namespace</summary>

  ```
  kubectl create namespace kafka
  ```
</details>

**Task:** Apply the [Strimzi operator](strimzi-cluster-operator.yaml) the the `kafka` namespace.
<details>
  <summary><strong>Hint</strong>: Apply Strimzi operator</summary>

  ```
  kubectl apply -n kafka -f strimzi-cluster-operator.yaml
  ```
</details>

**Task:** Wait for the completion of the deployment: `kubectl get pod -n kafka --watch`.


#### Deploy the Kafka cluster using Strimzi


**Task:** Apply the [Kafka manifest](kafka.yaml) to the `kafka` namespace.
<details>
  <summary><strong>Hint</strong>: Apply Kafka manifest</summary>

  ```
  kubectl apply -n kafka -f kafka.yaml
  ```
</details>



**Task:** Wait for the completion of the Kafka deployment: `kubectl wait kafka/strimzi --for=condition=Ready --timeout=300s -n kafka`.

#### Extra services

You will need extra services for interaction with Kafka. All of these are included in the [kafka-extra.yaml](kafka-extra.yaml) file. 

The list below summarises the extra services and briefly demonstrate how to interact with them:
- Kowl (kowl)
  - `kubectl port-forward svc/kowl  8080:8080 -n kafka`. Open [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser!
- Registry (kafka-schema-registry) 
  - `kubectl port-forward svc/kafka-schema-registry  8081:8081 -n kafka`. Make a curl in a terminal [http://127.0.0.1:8081](http://127.0.0.1:8081) and get this output:
    ```
    curl http://127.0.0.1:8083
    {}%                                  
    ```
- Connect (kafka-connect)
  - `kubectl port-forward svc/kafka-connect  8083:8083 -n kafka`. Make a curl in a terminal [http://127.0.0.1:8083](http://127.0.0.1:8083) and get this output:
    ```
    curl http://127.0.0.1:8083
    {"version":"7.3.1-ce","commit":"a453cbd27246f7bb","kafka_cluster_id":"ibXE6-pLRouRr7kLM6o_MQ"}%                                    
    ```
- KsqlDB (kafka-ksqldb-server)
- KsqlDB CLI (kafka-ksqldb-cli)
  - `kubectl exec --namespace=kafka --stdin --tty kafka-ksqldb-cli-<TODO>  -- ksql http://kafka-ksqldb-server:8088` make sure you will reach a console similar to this:
  **NB:** update the name `(kafka-ksqldb-cli-<TODO>)` of the container!

    ```
                      
                      ===========================================
                      =       _              _ ____  ____       =
                      =      | | _____  __ _| |  _ \| __ )      =
                      =      | |/ / __|/ _` | | | | |  _ \      =
                      =      |   <\__ \ (_| | | |_| | |_) |     =
                      =      |_|\_\___/\__, |_|____/|____/      =
                      =                   |_|                   =
                      =        The Database purpose-built       =
                      =        for stream processing apps       =
                      ===========================================

    Copyright 2017-2022 Confluent Inc.

    CLI v7.3.1, Server v7.3.1 located at http://kafka-ksqldb-server:8088
    Server Status: RUNNING

    Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

    ksql> 
    ```



**Task:** Apply the [Kafka-extra manifest](kafka-extra.yaml.yaml) to the `kafka` namespace.
<details>
  <summary><strong>Hint</strong>: Apply Kafka extra services manifest</summary>

  ```
  kubectl apply -n kafka -f kafka-extra.yaml
  ```
</details>



#### Validate in deployment of Kafka using a simple producer and consumer

**Task:** Open two different terminal windows.

**Task:** Run this cmd in the first terminal: `kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:0.37.0-kafka-3.5.1 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server strimzi-kafka-bootstrap:9092 --topic test`

**Task:** Run this cmd in the second terminal: `kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.37.0-kafka-3.5.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server strimzi-kafka-bootstrap:9092 --topic test --from-beginning`

**Task:** Explain what you see.

**Task:** Clean up. Exit each of the terminal windows and delete the two pods; `kafka-producer` and `kafka-consumer`.
<details>
  <summary><strong>Hint</strong>: Delete the two pods used for validating the deployment.</summary>

  ```
  kubectl delete pod/kafka-producer -n kafka
  kubectl delete pod/kafka-consumer -n kafka 
  ```
</details>

### Exercise 02 - Interacting with Kafka using Kowl
Open [http://127.0.0.1:8080](http://127.0.0.1:8080) in our browser!


- What does the Topics view [http://127.0.0.1:8080/topics](http://127.0.0.1:8080/topics) show you?
1. Use Kowl to create a topic called `test-kowl`.
1. Use Kowl to insert a JSON message with key=`1` and value=`{"id":1,"status":"it works"}` to the created topic `test-kowl`.
1. Use Kowl to delete the messages.

### Exercise 03 (optional) - Create topics on Kafka using the CLI
### Exercise 04 (optional) - Consume and produce messages on Kafka using the CLI
### Exercise 06 - Produce messages to Kafka using Python


We will rewrite [exercise 09](../02/exercises.md#exercise-9---create-six-fictive-data-sources) from the last lecture.
We would like to produce sensor samples to Kafka directly instead of writing sensor data directly to HDFS. Then we would like a Kafka Connector to persist the samples into HDFS directly from the `INGESTION` topic.


Questions prior to creating an `INGESTION` topic for this exercise
- How many partitions will du have?
- Which replication factor will you use?
- Which min in-sync replicas will you use?
- What would be an appropriate retention time?
- What would be an appropriate retention size?


**Task** Create the schema and publish it

WIP -> schema registry
**Task** Update the program to produce sensor samples to Kafka.





### Exercise 07 - Consume messages from Kafka using Python with single and multiple consumers

**Task** Write a consumer and print the messages from the `INGESTION` topic.

Questions:
- Produce some messages
- Start another consumer
- Do both consumers receive the same messages?
  - why?
  - why not?
- How can we get the consumers to receive the same messages?

### Exercise 08 - Kafka Ksql

use ksqlDB to split the messages in `INGESTION` topic into six separate streams `SENSOR-{01, 02, ..., 06}`.

`kubectl exec ` into ksqlDB: `kubectl exec --namespace=kafka --stdin --tty kafka-ksqldb-cli-<TODO>  -- ksql http://kafka-ksqldb-server:8088` make sure you will reach a console similar to this:

### Exercise 09 - Kafka Connect and HDFS

[HDFS3 sink](https://docs.confluent.io/kafka-connectors/hdfs3-sink/current/overview.html)

configure Kafka Connect to write the messages from the `INGESTION` topic into HDFS

### Exercise 10 (optional)  - Produce messages using the registry and a serializer producer

### Exercise 11 (optional)  - Produce messages from a file to Kafka using Flume

1. Check Documentation
    1. Flume user guide: [FlumeUserGuide](https://flume.apache.org/FlumeUserGuide.html)
    1. Examples of a flume configuration including a docker image can be found in [flume](./flume/)
    1. In the Dockerfile, there might be some changes required based on the chip architecture of your computer
    1. Try to publish Alice-in-wonderland.txt to kafka using flume.