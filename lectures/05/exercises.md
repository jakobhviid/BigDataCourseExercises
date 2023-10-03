# Lecture 05 - Distributed Data Processing and Distributed Databases

## Exercises

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!

Before you start working on the exercises you are strongly encouraged to clean up your Kubernetes cluster. The exercises will assume you use the MicroK8s cluster on the provided virtual machines and that the cluster is in a "clean" state.

### Exercise 1 - Set up Trino, Hive and Minio

[Trino](https://trino.io/) (formerly known as Presto) is a distributed SQL query engine for big data analytics. Trino is comparable to Apache Hive, but Trino can connect to many different data sources with [connectors](https://trino.io/docs/current/connector.html). Hive is also meant to run using YARN and it does not make sense to run YARN inside of Kubernetes. For that reason, the exercises will be about Trino.

You will be setting up a [Trino cluster](https://trino.io/docs/current/overview/concepts.html#cluster) and use the [Hive connector](https://trino.io/docs/current/connector/hive.html) to read files from an S3 bucket. An [Apache Hive metastore](https://cwiki.apache.org/confluence/display/hive/design#Design-Metastore) cluster is required in order to use the Hive connector. Hive metastore requires an SQL database to store data, so for this you will also set up a [PostgreSQL database](https://www.postgresql.org/).

You are also strongly encouraged to read [this](https://trino.io/Presto_SQL_on_Everything.pdf) paper about Trino, but it is not a requirement for the exercises.

#### Stackable operators

You will need the commons, secret, hive, and trino operators. We will create them inside the stackable namespace.

```text
kubectl create namespace stackable
helm repo add stackable-stable https://repo.stackable.tech/repository/helm-stable/
helm install -n stackable commons-operator stackable-stable/commons-operator --version 23.7.0
helm install -n stackable secret-operator stackable-stable/secret-operator --version 23.7.0 --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet
helm install -n stackable hive-operator stackable-stable/hive-operator --version 23.7.0
helm install -n stackable trino-operator stackable-stable/trino-operator --version 23.7.0
```

#### MinIO

Install MinIO

```text
helm install minio oci://registry-1.docker.io/bitnamicharts/minio --set service.type=NodePort --set auth.rootUser=admin --set auth.rootPassword=password
```

Create S3Connection that will be used by Hive metastore service to connect to MinIO.

Apply [s3connection.yaml](./s3connection.yaml).

#### Hive metastore service

The Hive metastore service will be deployed with PostgreSQL.

Deploy postgres database.

```text
helm install postgresql \
--version=12.1.5 \
--namespace default \
--set auth.username=hive \
--set auth.password=hive \
--set auth.database=hive \
--set primary.extendedConfiguration="password_encryption=md5" \
--repo https://charts.bitnami.com/bitnami postgresql
```

**Note:** You may have to delete the `\` and newlines so that it is one command.

Everything required to create the Hive cluster is now ready. Apply the [hive.yaml](./hive.yaml) file.

#### Trino cluster

Apply the [trino.yaml](./trino.yaml) file. This file contains the TrinoCluster resource and TrinoCatalog resource. The [TrinoCatalog resource](https://docs.stackable.tech/home/stable/trino/concepts#_catalogs) is used to create an instance of a connector, in this case it is a Hive connector. Not a lot of connectors are supported by Stackable, but it will suffice for these exercises.

### Exercise 2 - Count words in Alice in Wonderland with Hive
#### Exercise 2.1 - Internal table

exercise 3 from last time..

![Alt text](image.png) TOTO: to be deleted

#### Exercise 2.2 - External table


Exercise 5 from last time..


- Loose coupling with the data.
  - Why should we use Hive external tables?
  - Data can be managed by more that Hive.
  - To avoid that dropping tables in Hive deletes data. 
- Lets start out by cleaning up our Hive tables!
  - DROP TABLE word_counts, lines
  - SHOW TABLES; - verify the tables are gone 👀
- Upload alice-in-wonderland.txt to HDFS again. You can follow Exercise 1 if in doubt on how to do that.


- Lets create an external table!
  - CREATE EXTERNAL TABLE lines (line string) LOCATION 'hdfs://namenode:9000/txt'; 
- Now lets recreate the word_counts table
  - See previous slide.
  - Verify that it is recreated with SELECT * FROM word_counts ORDER BY count DESC LIMIT 10; 
- Now lets add another book into HDFS and query from them both!
  - hdfs dfs -put alice-in-wonderland.txt /txt/alice-in-wonderland2.txt on the namenode
  - SELECT COUNT(*) FROM lines;
  - SELECT INPUT__FILE__NAME FROM lines GROUP BY INPUT__FILE__NAME;
- What happened? What results did you see?

### Exercise 3 - Compute the mean value for each of the sensors using SQL


Look into previus exercise lecture 2 sensor data to HDFS. 

Compute the mean based on the avro files using an exeternal table.





### Exercise 4 - Compose a MongoDB cluster
The objective of this exercise is to interact with a NoSQL document-oriented database. 
We will be working with MongoDB which is great for storing JSON like records with or without schemas and the database is horizontal scalable.

**Note:** We will deploying the minimum configuration for this database in order to reduce the recoruse footprint. 

This exercise is composed of three parts starting wiht a deployment of the MongoDB cluster. Then we would like to revist Kafka Connect similar to [Exercise 06](./../03/exercises.md#exercise-06---kafka-connect-and-hdfs) from lecture 3. And finally we will look into querying JSON records in the database.


We recommand to create a isolated namespace for the following MongoDB services.

**Task:** Create a namepsace in Kubernetes called `mongodb`.
<details>
  <summary><strong>Hint:</strong> Create namespace</summary>

  ```
  kubectl create namespace mongodb 
  ```
  
</details>



The [mongodb.yaml](mongodb.yaml) contains a complete manifest to compose a MongoDB cluster. The manifest includes the following recources:
- PersistentVolumeClaim: `mongodb-pvc`
- Services
  - `mongodb`
    - type: NodePort
    - port: 27017 <-> 27017
  - `mongo-express`
    - type: NodePort
    - port: 8084 <-> 8084
- Deployments
  - `mongodb`
  - `mongo-express`

**Task:** Familize yourself with the [mongodb.yaml](mongodb.yaml) manifest.
**Note:** Our example includes a simple authentication mecanishm. The username and password have been hardcoded into the [mongodb.yaml](mongodb.yaml) file. We do encurge you to apply a more sufisticated approach when you transfering into a production environment. 


**Task:** Apply the [mongodb.yaml](mongodb.yaml) manifest to compose the MongoDB cluster.
<details>
  <summary><strong>Hint:</strong> Apply the deployment manifest</summary>

  ```
  kubectl apply -f mongodb.yaml
  ```

</details>



**Task:** Validate your deployment of MongoDB.

<details>
  <summary><strong>Hint:</strong> Get all the resources inside the `mongodb` namespace</summary>

  One approach for getting the current state of the deployed resources is by using the command below:


  ```
  kubectl get all -n mongodb  
  ```
  You should execept a similar output like the chunk below:

  ```
  NAME                               READY   STATUS    RESTARTS   AGE
  pod/mongodb-f585b897b-f7bn6        1/1     Running   0          7m31s
  pod/mongo-express-f896d549-5gbz7   1/1     Running   0          2m51s

  NAME                               TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
  service/mongodb                    NodePort   10.152.183.106   <none>        27017:32346/TCP   7m32s
  service/mongo-express              NodePort   10.152.183.163   <none>        8084:31280/TCP    7m32s

  NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
  deployment.apps/mongodb            1/1     1            1           7m32s
  deployment.apps/mongo-express      1/1     1            1           7m31s

  NAME                                     DESIRED   CURRENT   READY   AGE
  replicaset.apps/mongodb-f585b897b        1         1         1       7m31s
  replicaset.apps/mongo-express-f896d549   1         1         1       2m51s
  ```

</details>


#### Exercise 4.1 - Interact with MongoDB

We will briefly introduce two approaches for interacting with MongoDB. One approach is the web-based interface called `mongo-express` which is already included in the previously mentioned [mongodb.yaml](mongodb.yaml) manifest file. 
The other approach is to install an extension for Visual Studio Code. Get further information on the extension here: [MongoDB for VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode).


##### Web-based interface
The web-based `mongo-express` interface requires port-forwarding to access the site from your local host.

**Task:** Forward port `8084` from the `mongo-express` service to your local host.
<details>
  <summary><strong>Hint:</strong> Get all the resources inside the `mongodb` namespace</summary>

  ```
  kubectl port-forward svc/mongo-express  8084:8084 -n mongodb
  ```
</details>


**Task:** Open [127.0.0.1:8084](http://127.0.0.1:8084) and validate the hostname of the mongodb server. Does the server name match the name of the `mongodb` Kubernetes pod?

**Note:** You will be prompted for a username and password. Please use `admin` and `pass` as log-in credentials respectively.

**Task:** Explore the `mongodb` documentation [here](https://www.mongodb.com/docs/manual/core/databases-and-collections/) and be confident in the MongoDB terminology, e.g. document, collection, and databases.

**Task:** Explore the `mongo-express` documentation [here](https://github.com/mongo-express/mongo-express) and be curious about the web-based interface [127.0.0.1:8084](http://127.0.0.1:8084).


##### MongoDB extension for Visual Studio Code

Another convenient approach for interacting with MongoDB is by using Visual Studio Code as a NoSQL editor. You can enable this feature by installing the [MongoDB for VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode) extension. 

Similar to the web-based approach you need to set up port-forwarding to reach the `mongodb` pod from your local host.

**Task:** Forward port `27017` from the `mongodb` service to your local host.
<details>
  <summary><strong>Hint:</strong> Get all the resources inside the `mongodb` namespace</summary>

  ```
  kubectl port-forward svc/mongodb  27017:27017 -n mongodb 
  ```
</details>

After the completion of the port-forwarding, you are able to insert the following connection string in the MongoDB for VS Code extension: `mongodb://admin:password@127.0.0.1:27017`

**Task:** Establish the connection to MongoDB using the extension.

**Task:** Explore the playgrounds tab inside the extension. Click "Create New Playground" and execute the new playground.

**Task:** Explore the newly created database called `mongodbVSCodePlaygroundDB` and the inserted documents inside the `sales` collections. You should find the identical documents inside the web interface [here](http://127.0.0.1:8084/db/mongodbVSCodePlaygroundDB/sales).


#### Exercise 4.2 - MongoDB and Kafka connect
Multiple approaches for interfacing with MongoDB have been covered in the previous section. Now you need to fill documents into the database before writing queries on the documents.

The objective of this exercise is to configure a Kafka Connect connector that uses the `INGESTION` topic as a source and MongoDB as a sink. Therefore the exercise assumes you have records inside the `INGESTION` topic. 

**Task:** If the `INGESTION` topic is empty we recommend revisiting [Exercise 03](./../03/exercises.md#exercise-03---produce-messages-to-kafka-using-python) from lecture 3 and re-establish the Kafka produce to create new records.

**Task:** Configure a Kafka Connect connector to move records from Kafka to MongoDB.

**Hint:** This task can be solved with multiple approaches. Please start by revisiting the concept in [Exercise 06](./../03/exercises.md#exercise-06---kafka-connect-and-hdfs) from lecture 3.

**Hint:** Then read the documentation here: [Configure the Sink Connector](https://www.mongodb.com/docs/kafka-connector/current/tutorials/sink-connector/#configure-the-sink-connector). The documentation suggests to post the configuration to the Kafka Connect REST API, which is similar to the approach in [Exercise 06](./../03/exercises.md#exercise-06---kafka-connect-and-hdfs).

**NB:** Remember to setup port-forwarding for the Kafka Connect REST API.

<details>
  <summary><strong>Hint:</strong> Post configuration</summary>

    This example requires port-forwarding. Therefore ensure `kubectl port-forward svc/kafka-connect 8083:8083 -n kafka` is running in a terminal on your local host.

    Look into the configuration in the chunk below and execute the command in your terminal to create a Kafka Connect connector:

```sh
curl -X POST \
http://127.0.0.1:8083/connectors \
-H 'Content-Type: application/json' \
-d '{
    "name": "mongodb-sink",
    "config": {
        "connection.password": "password",
        "connection.uri": "mongodb://admin:password@mongodb.mongodb:27017",
        "connection.url": "mongodb://mongodb.mongodb:27017",
        "connection.username": "admin",
        "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
        "database": "kafka",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "key.converter.schemas.enable": "true",
        "name": "mongodb-sink-connector-cdfs",
        "output.format.key": "json",
        "output.format.value": "json",
        "post.processor.chain": "com.mongodb.kafka.connect.sink.processor.DocumentIdAdder",
        "tasks.max": "4",
        "timeseries.timefield.auto.convert": "false",
        "topics": "INGESTION",
        "value.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter.schemas.enable": "true"
    }
}'
```
</details>


**Task:** Validate that the connector is running. Please count the number of documents inside the `INGESTION` collection. Does it match the number of records inside your `INGESTION` topic in [redpanda](http://127.0.0.1:8080/topics/INGESTION#messages)?


<details>
  <summary><strong>Hint:</strong> Count number of documents</summary>
  You need to open a new playground in MongoDB for the VS Code extension to reproduce this hint.

  The playground result of the chuck below will return the number of documents inside the `INGESTION` collection.

  ```js
  use('kafka');
  db.getCollection('INGESTION').countDocuments();
  ```
</details>


#### Exercise 4.3 - Query Documents in MongoBD
We are finally ready to start querying the documents inside MongoDB to answer important questions about the dataset.

You may find this documentation helpful to complete this exercise.
- [Query Documents](https://www.mongodb.com/docs/manual/tutorial/query-documents/#query-documents)
- [$regex](https://www.mongodb.com/docs/manual/reference/operator/query/regex/#-regex)

**Task:** Count the number of documents inside the `INGESTION` collection where the `sensor_id=6`.

<details>
  <summary><strong>Hint:</strong> Count number of documents for sensor_id six </summary>
  You need to open a new playground in MongoDB for the VS Code extension to reproduce this hint.

  The playground result of the chuck below will return the number of documents inside the `INGESTION` collection.

  ```js
  use('kafka');
  db.getCollection('INGESTION').find({ "payload": { $regex: /^{\"sensor_id\": 6/ } }).count();
  ```
</details>

**Task:** Formulize a question to answer about the documents in MongoDB and create a proper query to answer this question. Post the question and your solution in our Discord channel called "exercises".