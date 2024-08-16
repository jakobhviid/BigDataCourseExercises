# Lecture 03 - Distributed Transport and Streaming


## Exercises

The exercises for this week's lecture will be about distributed transport and streaming. You will be creating a Kafka cluster and various publishing programs and subscribing programs to stream records.
The focus of today's lecture is to interact with Kafka, create Python producer and consumer programs, and configure Kafka connect modules. 

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!


### Exercise 1 - Composing a Kafka cluster



helm install kafka oci://registry-1.docker.io/bitnamicharts/kafka






The objective of this exercise is to deploy a Kafka cluster. We will be using operators from a company called [strimzi.io](http://strimzi.io). The image below links to a short introductory video on how to set up Kafka inside Kubernetes. 

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/1qO2qGuJNQI/0.jpg)](https://www.youtube.com/watch?v=1qO2qGuJNQI)

For the remaining steps of this exercise is to copy and paste commands into the terminal.


#### Essential files

We have chosen to fetch the manifest files to remove an external dependencies. Therefore we recommend you familiarize yourself with the two mentioned files: 

- [kafka.yaml](./kafka.yaml)
- [kafka-extra.yaml](kafka-extra.yaml)

**NB:** Make sure your terminal path is relative to these files before moving forward.

#### Deploy Strimzi

**Task:** Create namespace `kafka` in Kubernetes.
<details>
  <summary><strong>Hint:</strong> Create Kubernetes namespace</summary>

  ```
  kubectl create namespace kafka
  ```
</details>

**Task:** Install the [Strimzi operator](https://artifacthub.io/packages/helm/strimzi/strimzi-kafka-operator) in the `kafka` namespace.

**Note:** The Strimzi operator should be installed with the value `watchAnyNamespace=true`. If not, then you can only create Kafka clusters inside the same namespace that you install the operator inside.

<details>
  <summary><strong>Hint:</strong> Install Strimzi operator</summary>

  ```
  helm install -n kafka strimzi-cluster-operator oci://quay.io/strimzi-helm/strimzi-kafka-operator --set watchAnyNamespace=true
  ```
</details>

**Task:** Wait for the completion of the deployment: `kubectl get pod -n kafka --watch`.


#### Deploy the Kafka cluster using Strimzi

Now that the Strimzi operator is installed and running you can now create the Kafka cluster.

**Task:** Apply the [Kafka manifest](kafka.yaml) to the `kafka` namespace.
<details>
  <summary><strong>Hint:</strong> Apply Kafka manifest</summary>

  ```
  kubectl apply -n kafka -f kafka.yaml
  ```
</details>



**Task:** Wait for the completion of the Kafka deployment: `kubectl wait kafka/strimzi --for=condition=Ready --timeout=300s -n kafka`.

#### Extra services

You need extra services to interact with Kafka. All of these services are included in the [kafka-extra.yaml](kafka-extra.yaml) file.

**Task:** Apply the [Kafka-extra manifest](kafka-extra.yaml.yaml) to the `kafka` namespace.
<details>
  <summary><strong>Hint:</strong> Apply Kafka extra services manifest</summary>

  ```
  kubectl apply -n kafka -f kafka-extra.yaml
  ```
</details>

The list below summarises the extra services and briefly demonstrate how to interact with them:
- Redpanda (redpanda)
  - `kubectl port-forward svc/redpanda  8080:8080 -n kafka`. Open [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser!
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
  - `kubectl exec --namespace=kafka --stdin --tty deployment/kafka-ksqldb-cli -- ksql http://kafka-ksqldb-server:8088` make sure you will reach a console similar to this:

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

#### Validate in deployment of Kafka using a simple producer and consumer


**Tasks:** Producing and consuming topic messages

1. Run this command in a terminal: `kubectl -n kafka run kafka-producer -it --rm --image=quay.io/strimzi/kafka:0.37.0-kafka-3.5.1 -- bin/kafka-console-producer.sh --bootstrap-server strimzi-kafka-bootstrap:9092 --topic test`
2. Run this command in another terminal: `kubectl -n kafka run kafka-consumer-1 -it --rm --image=quay.io/strimzi/kafka:0.37.0-kafka-3.5.1 -- bin/kafka-console-consumer.sh --bootstrap-server strimzi-kafka-bootstrap:9092 --topic test`
3. Try typing text in the first terminal and hit enter
4. Look at the second terminal. What happened?

**Task:** Delete the two pods you just created (`kafka-producer` and `kafka-consumer`).

<details>
  <summary><strong>Hint:</strong> Delete the pods</summary>

  CTRL + C should exit the terminal and delete the pods. If not then just use the commands below.

  ```
  kubectl delete -n kafka pod/kafka-producer
  kubectl delete -n kafka pod/kafka-consumer
  ```
</details>

### Exercise 2 - Using Redpanda to interact with Kafka
The objective of this exercise is to use [Redpanda Console](https://redpanda.com/redpanda-console-kafka-ui) for interacting with Kafka.
Open Redpanda at [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser!

**Task:** Explore the following tabs:
- [Overview](http://127.0.0.1:8080/overview)
- [Topics](http://127.0.0.1:8080/topics)
- [Schema Registry](http://127.0.0.1:8080/schema-registry)
- [Kafka Connectors](http://127.0.0.1:8080/connect-clusters/Connectors)

<details>
  <summary><strong>Hint:</strong> Do port-forward in order to access Redpanda.</summary>
  
  Do the following in a terminal: `kubectl port-forward svc/redpanda  8080:8080 -n kafka` and then nagivate to [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser!
 
</details>

 
**Task:** Question: What does the Topics view [http://127.0.0.1:8080/topics](http://127.0.0.1:8080/topics) show you?

**Task:** Manual interaction with Kafka using Redpanda UI:
1. Use Redpanda to create a topic called `test-redpanda`.
1. Use Redpanda to insert a JSON message with key=`1` and value=`{"id":1,"status":"it works"}` to the created topic `test-redpanda`.
1. Use Redpanda to delete all the messages in topic `test-redpanda`.

<details>
  <summary><strong>Hint:</strong> Step by step.</summary>

  1. A new topic can be generated by clicking on the "Create Topic" button inside the [Topics view](http://127.0.0.1:8080/topics).
  1. Find the button "Actions" and "Publish Message" inside the newly generated topic `test-redpanda`: [topics/test-redpanda](http://127.0.0.1:8080/topics/test-redpanda). Add the proper key for the message under "key" view and add the json value under "value". Press "Publish" to complete.
  1. Find the button "Actions" and "Delete Records" inside the newly generated topic `test-redpanda`: [topics/test-redpanda](http://127.0.0.1:8080/topics/test-redpanda). Select "All Partitions" -> press "Choose End Offset" -> select "High Watermark" -> press "Delete Recrods" -> done.
 
</details>



### Exercise 3 - Produce messages to Kafka using Python

The objective of this exercise is to create a program which publishes messages to a Kafka topic. The exercise builds on top of [exercise 9 from lecture 2](../02/exercises.md#exercise-9---create-six-fictive-data-sources), but instead of saving the data to HDFS we will publish it to a Kafka topic and use a Kafka Connector to save the samples to HDFS. 
This exercise focuses on creating the topic and creating the producer. If you have not solved the exercise from last week then you can use the files provided [here](./hints/simple-producer.py).

**Tasks:** Think about what settings you want for the `INGESTION` topic:

- How many partitions will you have for the `INGESTION` topic?
- Which replication factor will you use for the `INGESTION` topic?
- Which min in-sync replicas will you use for the `INGESTION` topic?
- What would be an appropriate retention time for the `INGESTION` topic?
- What would be an appropriate retention size for the `INGESTION` topic?

**Task:** Create the `INGESTION` topic with your chosen properties.

**Hint:** Use Redpanda (ref. [exercise 02](#exercise-02---using-redpanda-to-interact-with-kafka)).

**Task:** Question: Which property will be possible if you add a key, which defines the sensor id, to each records?

**Task:** Update your program from [lecture 2 exercise 9](../02/exercises.md#exercise-9---create-six-fictive-data-sources) to produce sensor samples directly to Kafka.

**Hint:** If you did not create a program then use the scripts [here](./hints/).

**Hint:** Create an Ubuntu container and attach to it using [vscode](../02/exercises.md#attach-visual-studio-code-to-an-interactive-container-in-kubernetes).

Now that you have created the program it is time to run it.

**Task:** Run the program

To verify that the program is producing messages to the `INGESTION` topic. Open [redpanda](http://127.0.0.1:8080/topics/INGESTION?p=-1&s=50&o=-1#messages).

<details>
  <summary><strong>Hint:</strong> Python producer</summary>

  1. Install Python inside the interactive container using `sudo apt update && sudo apt install python -y`
  2. Copy the provided solution to the interactive container
     - [client.py](./hints/client.py)
     - [data_model.py](./hints/data_model.py)
     - [simple-producer.py](./hints/simple-producer.py)
  3. Run the program using `python simple-producer.py`

  Open [http://127.0.0.1:8080/topics/INGESTION](http://127.0.0.1:8080/topics/INGESTION#messages) in your browser and look for the number of messages.
 
</details>

### Exercise 4 - Consume messages from Kafka using Python with single and multiple consumers

The objective of this exercise is to write a Python consumer and to print the messages from the `INGESTION` topic.

A requirement for the program is that it must take a consumer `group_id` as an argument. It can either be an environment variable, a config file, or an argument to the program when you run it.

<details>
  <summary><strong>Hint:</strong> Simple consumer program.</summary>

  The below mentioned files provide one solution for exercise.

  - [client.py](./hints/client.py)
  - [data_model.py](./hints/data_model.py) (not used but is still required because it is imported by `client.py`)
  - [simple-consumer.py](./hints/simple-consumer.py)

  </details>

**Task:** Start the default consumer in the terminal in your interactive container.


<details>
  <summary><strong>Hint:</strong> Default consumer.</summary>

  Run the program using `python simple-consumer.py`

  The following should be printed to the console:
  
  ```
  group_id=DEFAULT_CONSUMER
  PackageObj(payload=SensorObj(sensor_id=3, modality=421, unit='MW', temporal_aspect='real_time'), correlation_id='906f764e-0f3b-4517-aed7-3b646081f6fb', created_at=1694902173.122458, schema_version=1)
  ...
  ...
  ...
  ```

  </details>
  
**Task:** Start another consumer but with a different group id in your interactive container.

<details>
  <summary><strong>Hint:</strong> Another consumer</summary>

  Run the program using `python simple-consumer.py <GROUP_ID>`

  The following should be printed to the console:

  ```
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

### Exercise 5 - Kafka Ksql

The objective of this exercise is use ksqlDB to split the records in the `INGESTION` topic into six separate streams ` SENSOR_ID_{1, 2, ..., 6}` based on the sensor id in the `payload` field of the JSON file.


#### Useful ksqlDB commands

- `SHOW TOPICS;`
- `PRINT <topic> FROM BEGINNING;`
- `SHOW STREAMS;`
- `CREATE STREAM ...`

**Task:** Get interactive shell with ksqlDB.

<details>
  <summary><strong>Hint:</strong> kubectl exec</summary>

  This was already explained [here](#extra-services), but see the command below:

  ```
  kubectl exec --namespace=kafka --stdin --tty deployment/kafka-ksqldb-cli -- ksql http://kafka-ksqldb-server:8088
  ```
 
</details>


**Task:** Create a stream over the exsiting `INGESTION` topic with the following name `STREAM_INGESTION`.


<details>
  <summary><strong>Hint:</strong>ksqlDB CREATE STREAM on topic</summary>

  ```sql
  CREATE STREAM STREAM_INGESTION (
    payload STRING,
    correlation_id STRING,
    created_at DOUBLE,
    schema_version INTEGER
) WITH (KAFKA_TOPIC = 'INGESTION', VALUE_FORMAT = 'JSON');
  ```
 
</details>

**Task:** Create a new stream based on previously created stream `STREAM_INGESTION`. Start by writing a SQL statement which filters the records with the sensor of interest. Then populate the records into a new stream `SENSOR_ID_<sensor_id>`.

<details>
  <summary><strong>Hint:</strong> ksqlDB CREATE STREAM from SELECT</summary>

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




**Task:** Validate your newly created streams using ksql commands in the CLI and see their belonging topic in [Redpanda UI](http://127.0.0.1:8080/topics).



### Exercise 6 - Kafka Connect and HDFS
The objective of this exercise is apply and configure a Kafka Connect module to write the records from the `INGESTION` topic into HDFS as mentioned in [exercise 03](#exercise-03---produce-messages-to-kafka-using-python).

The module of interest is the [HDFS 2 Sink Connector](https://docs.confluent.io/kafka-connectors/hdfs/current/overview.html) created by a company called Confluent. The module will be accessible through the ready-running `kafka-connect` service. The creation of the underlying image of our `kafka-connect` service can be further explored here: [kafka-connect - README.md](../../services/kafka-connect/README.md). 
***NB:*** This connector module will work with our installation of HDFS despite the various version numbers. This module is under the [Confluent Community License v1.0](https://www.confluent.io/confluent-community-license/) which enables free use.


**Task:** Setup HDFS 2 Sink Connector in our kafka-connect service.
***NB:*** Redpanda UI does not include all the necessary properties for the configuration of the HDFS 2 Sink Connector. Therefore you need to investigate how to interact with the [Connect REST Interface](https://docs.confluent.io/platform/current/connect/references/restapi.html). Then you need to post the configuration using `curl` in a terminal with port-forwarding enabled or using an interactive container in Kubernetes.

  <details>
    <summary><strong>Hint:</strong>Post the configuration using curl</summary>

    This example will be using port-forwarding. Therefore ensure `kubectl port-forward svc/kafka-connect 8083:8083 -n kafka` has been enabled.

    Look into the configuration in the chunk below and the command in your terminal:

    ```sh
    curl -X POST \
    http://127.0.0.1:8083/connectors \
    -H 'Content-Type: application/json' \
    -d '{
        "name": "hdfs-sink",
        "config": {
            "connector.class": "io.confluent.connect.hdfs.HdfsSinkConnector",
            "tasks.max": "5",
            "topics": "INGESTION",
            "hdfs.url": "hdfs://simple-hdfs-namenode-default-0.default:8020",
            "flush.size": "3",
            "format.class": "io.confluent.connect.hdfs.json.JsonFormat",
            "key.converter.schemas.enable":"false",
            "key.converter": "org.apache.kafka.connect.storage.StringConverter",
            "key.converter.schema.registry.url": "http://kafka-schema-registry.kafka:8081", 
            "value.converter.schemas.enable":"false",
            "value.converter.schema.registry.url": "http://kafka-schema-registry.kafka:8081", 
            "value.converter": "org.apache.kafka.connect.json.JsonConverter"
        }
    }'
    ```
  </details>


**Task:** Validate the HDFS 2 Sink Connector is working as expected.
- Make sure the following folders in HDFS have been created: `/topics` and `/logs`.

  <details>
    <summary><strong>Hint:</strong>Post the configuration using curl</summary>

    - Open and interactive terminal like `kubectl run hdfs-cli -i --tty --image apache/hadoop:3 -- bash` and remember to set username `export HADOOP_USER_NAME=stackable`
    - `hdfs dfs -fs hdfs://simple-hdfs-namenode-default-0:8020 -ls /` -> `/topics` and `/logs`
    - `hdfs dfs -fs hdfs://simple-hdfs-namenode-default-0:8020 -ls /topics/` -> /topics/INGESTION
  </details>

- Use Redpanda UI to find the total lag (difference between log ned offset and group offset) of the consumer group `connect-hdfs-sink` [here](http://127.0.0.1:8080/groups/connect-hdfs-sink).
  - How does HDFS 2 Sink Connector keep up with the six fictive data sources?
