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
    curl http://127.0.0.1:8081
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

### Exercise 02 - Using Kowl to interact with Kafka
The objective of this exercise is to use Kowl for interacting with Kafka.
Open Kowl at [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser!

**Task:** Explore the following tabs:
- [Brokers](http://127.0.0.1:8080/brokers)
- [Topics](http://127.0.0.1:8080/topics)
- [Schema Registry](http://127.0.0.1:8080/schema-registry)
- [Kafka Connect](http://127.0.0.1:8080/kafka-connect)

<details>
  <summary><strong>Hint</strong>: Do port-forward in order to access Kowl.</summary>
  
  Do the following in a terminal: `kubectl port-forward svc/kowl  8080:8080 -n kafka` and then nagivate to [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser!
 
</details>

 
**Task:** Question: What does the Topics view [http://127.0.0.1:8080/topics](http://127.0.0.1:8080/topics) show you?

**Task:** Manual interaction with Kafka using Kowl:
1. Use Kowl to create a topic called `test-kowl`.
1. Use Kowl to insert a JSON message with key=`1` and value=`{"id":1,"status":"it works"}` to the created topic `test-kowl`.
1. Use Kowl to delete all the messages in topic `test-kowl`.

<details>
  <summary><strong>Hint</strong>: Step by step.</summary>

  1. A new topic can be generated by clicking on the "Create Topic" button inside the [Topics view](http://127.0.0.1:8080/topics).
  1. Find the button "Actions" and "Publish Message" inside the newly generated topic `test-kowl`: [topics/test-kowl](http://127.0.0.1:8080/topics/test-kowl). Add the proper key for the message under "key" view and add the json value under "value". Press "Publish" to complete.
  1. Find the button "Actions" and "Delete Records" inside the newly generated topic `test-kowl`: [topics/test-kowl](http://127.0.0.1:8080/topics/test-kowl). Select "All Partitions" -> press "Choose End Offset" -> select "High Watermark" -> press "Delete Recrods" -> done.
 
</details>



### Exercise 03 - Produce messages to Kafka using Python
The objective of this exercise is to create a Python program which procduces records to Kafka. The context of this excerise is identical to [exercise 09](../02/exercises.md#exercise-9---create-six-fictive-data-sources) from the last lecture. However, we would like to rewrite python program to produce sensor samples to Kafka directly instead of writing sensor data directly to HDFS. 
We will later use a Kafka Connector in [exercise 06](#exercise-06---kafka-connect-and-hdfs) to persist the samples into HDFS directly from the `INGESTION` topic.


**Task:** Questions prior to creating an `INGESTION` topic for this exercise:
- How many partitions will you have for the `INGESTION` topic?
- Which replication factor will you use for the `INGESTION` topic?
- Which min in-sync replicas will you use for the `INGESTION` topic?
- What would be an appropriate retention time for the `INGESTION` topic?
- What would be an appropriate retention size for the `INGESTION` topic?

**Task:** Use Kowl ([exercise 02](#exercise-02---using-kowl-to-interact-with-kafka)) to create the `INGESTION` topic with the chosen properties.

**Task:** Question: 
- Which property will be possible if you add a key, which defines the sensor id, to each records?

**Task:** Update the program to produce sensor samples directly to Kafka.
**Hint:** Develop the program using an interactive container running the Kubernetes.

**Task:** Validate the number of records are increasing inside the Kowl UI. 

<details>
  <summary><strong>Hint</strong>: Three python files.</summary>

  The below mentioned files provide one solution for exercise.

  - [client.py](./hints/client.py)
  - [data_model.py](./hints/data_model.py)
  - [simple-producer.py](./hints/simple-producer.py)

  ```
  cd ./hints/
  python simple-producer.py
  ```

  - Open [http://127.0.0.1:8080/topics/INGESTION](http://127.0.0.1:8080/topics/INGESTION#messages) in your browser and look for the number of messages.
 
</details>



### Exercise 04 - Consume messages from Kafka using Python with single and multiple consumers

The objective of this exercise is to write a Python consumer and to print the messages from the `INGESTION` topic.

**Requriments:** 

- The program must take accept a consumer group id at runtime, either by setting an environment variable or an input variable.

<details>
  <summary><strong>Hint</strong>: Simple consumer program.</summary>

  The below mentioned file provide one solution for exercise.

  - [simple-consumer.py](./hints/simple-consumer.py)

  </details>


**Task:** Start the default consumer in the terminal in your interactive container.


<details>
  <summary><strong>Hint</strong>: Default consumer.</summary>

  ```
  cd ./hints/
  python simple-consumer.py
  
  group_id=DEFAULT_CONSUMER
  PackageObj(payload=SensorObj(sensor_id=3, modality=421, unit='MW', temporal_aspect='real_time'), correlation_id='906f764e-0f3b-4517-aed7-3b646081f6fb', created_at=1694902173.122458, schema_version=1)
  ...
  ...
  ...
  ```

  </details>
  
**Task:** Start a consumer with given name in another terminal in your interactive container.


<details>
  <summary><strong>Hint</strong>: Given consumer group.</summary>

  ```
  cd ./hints/
  python simple-consumer.py <GROUP_ID>

  group_id=<GROUP_ID>
  PackageObj(payload=SensorObj(sensor_id=3, modality=421, unit='MW', temporal_aspect='real_time'), correlation_id='906f764e-0f3b-4517-aed7-3b646081f6fb', created_at=1694902173.122458, schema_version=1)
  ...
  ...
  ...
  ```
 
</details>

**Task:** Open [http://127.0.0.1:8080/topics/INGESTION](http://127.0.0.1:8080/topics/INGESTION#consumers). You should now see a table similar to the one below. What does the Lag column mean?
```
Group               Lag
<GROUP_ID>          3182
DEFAULT_CONSUMER    3186
```

**Task:** Questions:

- How can we get two consumers to receive identical records?
- How can we get two consumers to receive unique records?
- What defines the maximum number of active parallel consumers within one consumer group?

### Exercise 05 - Kafka Ksql

The objective of this exercise is use ksqlDB to split the records in the `INGESTION` topic into six separate streams ` SENSOR_ID_{1, 2, ..., 6}` based on the sensor id in the payload.


#### Useful ksqlDB commands

- `SHOW TOPICS;`
- `SHOW STREAMS;`
- `PRINT <topic> FROM BEGINNING;`
- `CREATE STREAM ...`

**Task:** `kubectl exec` into the ksqlDB CLI.

<details>
  <summary><strong>Hint</strong>:kubectl exec</summary>

  ```
  kubectl exec --namespace=kafka --stdin --tty kafka-ksqldb-cli-<TODO> -- ksql http://kafka-ksqldb-server:8088
  ```
 
</details>


**Task:** Create a stream over the exsiting `INGESTION` topic with the following name `STREAM_INGESTION`.


<details>
  <summary><strong>Hint</strong>:ksqlDB CREATE STREAM on topic</summary>

  ```sql
  CREATE STREAM STREAM_INGESTION (
    payload STRING,
    correlation_id STRING,
    created_at DOUBLE,
    schema_version INTEGER
) WITH (KAFKA_TOPIC = 'INGESTION', VALUE_FORMAT = 'JSON');
  ```
 
</details>

**Task:** Create a new stream based on previously created stream `STREAM_INGESTION`. Start by writing a SQL statement which filters the records with the sensor of interest. 

<details>
  <summary><strong>Hint</strong>: ksqlDB CREATE STREAM from SELECT</summary>

  ```sql
  CREATE STREAM SENSOR_ID_<sensor_id> AS
  SELECT
      *
  FROM
      STREAM_INGESTION
  WHERE
      EXTRACTJSONFIELD(PAYLOAD, '$.sensor_id') = '<sensor_id>';
  ```
 
</details>




**Task:** Validate your newly created streams and belonging topic in [Kowl](http://127.0.0.1:8080/topics).



### Exercise 06 - Kafka Connect and HDFS

[HDFS3 sink](https://docs.confluent.io/kafka-connectors/hdfs3-sink/current/overview.html)

configure Kafka Connect to write the messages from the `INGESTION` topic into HDFS


```


```


```bash
curl -X POST \
http://kafka-connect.kafka:8083/connectors \
-H 'Content-Type: application/json' \
-d '{
"name": "hdfs-sink",
"config": {
"connector.class": "io.confluent.connect.hdfs.HdfsSinkConnector",
    "tasks.max": "5",
    "topics": "INGESTION",
    "hdfs.url": "hdfs://simple-hdfs-namenode-default-0.default:8020",
    "flush.size": "3",
    "key.converter.schema.registry.url": "http://kafka-schema-registry.kafka:8081", 
    "value.converter.schema.registry.url": "http://kafka-schema-registry.kafka:8081", 
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "format.class": "io.confluent.connect.hdfs.json.JsonFormat",
    "value.converter.schemas.enable":"false"
}
}'
```


kubectl run hdfs-cli -i --tty --image apache/hadoop:3 -- bash

hdfs dfs -fs hdfs://simple-hdfs-namenode-default-0:8020 -ls /topics/INGESTION/*



### Exercise 07 (optional)  - Produce messages from a file to Kafka using Flume

1. Check Documentation
    1. Flume user guide: [FlumeUserGuide](https://flume.apache.org/FlumeUserGuide.html)
    1. Examples of a flume configuration including a docker image can be found in [flume](./flume/)
    1. In the Dockerfile, there might be some changes required based on the chip architecture of your computer
    1. Try to publish Alice-in-wonderland.txt to kafka using flume.