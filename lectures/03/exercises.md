# Lecture 03 - Distributed Transport and Streaming


## Exercises

The exercises for this week's lecture will be about distributed transport and streaming. You will be creating a Kafka cluster and various publishing programs and subscribing programs for streams of records.
The focus of today's lecture is to interact with Kafka, create Python producer and consumer programs, and configure Kafka connect modules. 

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if ou encounter unclear information or experience bugs in our examples!


### Exercise 01 - Composing a Kafka Cluster


[https://strimzi.io/quickstarts/](https://strimzi.io/quickstarts/)

#### Essential files

- [strimzi-cluster-operator.yaml](./strimzi-cluster-operator.yaml)
- [kafka.yaml](./kafka.yaml)
- [kafka-extra.yaml](kafka-extra.yaml)


**Tasks**

Desc wip
```
kubectl create namespace kafka
```

Desc wip
```
kubectl apply -n kafka -f strimzi-cluster-operator.yaml
```

Desc wip
```
kubectl wait kafka/strimzi --for=condition=Ready --timeout=300s -n kafka
```
Desc wip
```
kubectl apply -n kafka -f kafka.yaml
```
Desc wip
```
kubectl apply -n kafka -f kafka-extra.yaml
```


#### Validate - Consume and produce message on Kafka using the CLI

Add a producer and a consumer in two different terminals
```
kubectl -n kafka run kafka-producer -ti --image=quay.io/strimzi/kafka:0.37.0-kafka-3.5.1 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server strimzi-kafka-bootstrap:9092 --topic test
```
```
kubectl -n kafka run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.37.0-kafka-3.5.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server strimzi-kafka-bootstrap:9092 --topic test --from-beginning
```

after validation -> clean up
```
kubectl delete pod/kafka-producer -n kafka
kubectl delete pod/kafka-consumer -n kafka 
```


##### Optional validations

Create port forwarding to these three services:
```
kubectl port-forward svc/kowl  8080:8080 -n kafka
kubectl port-forward svc/kafka-schema-registry  8081:8081 -n kafka
kubectl port-forward svc/kafka-connect  8083:8083 -n kafka 
```
and open [http://127.0.0.1:8080](http://127.0.0.1:8080) in our browser!


make a curl on [http://127.0.0.1:8081](http://127.0.0.1:8081) and get this output
```
curl http://127.0.0.1:8081
{}%                                  
```

make a curl on [http://127.0.0.1:8083](http://127.0.0.1:8083) and get this output
```
curl http://127.0.0.1:8083
{"version":"7.3.1-ce","commit":"a453cbd27246f7bb","kafka_cluster_id":"ibXE6-pLRouRr7kLM6o_MQ"}%                                   
```

`kubectl exec ` into ksqlDB: `kubectl exec --namespace=kafka --stdin --tty kafka-ksqldb-cli-<TODO>  -- ksql http://kafka-ksqldb-server:8088` make sure you will reach a console similar to this:

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

**NB:** update the name of the container



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