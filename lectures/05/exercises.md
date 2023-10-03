# Lecture 05 - Distributed Data Processing and Distributed Databases


## Exercises

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!

### Exercise 1 - Compose Apache Hive cluster

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
  <summary><strong>Hint</strong>: Create namespace</summary>

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
  <summary><strong>Hint</strong>: Apply the deployment manifest</summary>

  ```
  kubectl apply -f mongodb.yaml
  ```

</details>



**Task:** Validate your deployment of MongoDB.

<details>
  <summary><strong>Hint</strong>: Get all the resources inside the `mongodb` namespace</summary>

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

We will briefly introduce two approaches for interacting with MongoDB. One approach being the web-based interface called `mongo-express` which is already included in previously mentioned [mongodb.yaml](mongodb.yaml) manifest file. 
The other approach is to install an extension for Visual Studio Code. Get further information on the extension here: [MongoDB for VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode).


##### Web-based interface
The web-based `mongo-express` interface requries a port-forwarding in order to access the site from your localhost.

**Task:** Forward port `8084` from the `mongo-express` service to your localhost.
<details>
  <summary><strong>Hint</strong>: Get all the resources inside the `mongodb` namespace</summary>

  ```
  kubectl port-forward svc/mongo-express  8084:8084 -n mongodb
  ```
</details>


**Task:** Open [127.0.0.1:8084](http://127.0.0.1:8084) and validate the hostname of the mongodb server. Does the server name match the name of the `mongodb` Kubernetes pod?

**Note:** You will be prompted for a username and password. Please use `admin` and `pass` respectively.


**Task:** Explore the `mongodb` documentation [here](https://www.mongodb.com/docs/manual/core/databases-and-collections/) and be confidence in the MongoDB termonolygi, e.g. document, collection, and databases.

**Task:** Explore the `mongo-express` documentation [here](https://github.com/mongo-express/mongo-express) and be curious inside the web-based interface [127.0.0.1:8084](http://127.0.0.1:8084).


##### MongoDB extension for Visual Studio Code

Another convienct approach for interacting with MongoDB is by uing an Visual Studio Code as a NoSQL editor. You can enable this feature by installing the [MongoDB for VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode) extension. 

Similar to the web-based approach you need to setup port-farwarding in order to reach the `mongodb` pod from your localhost.

**Task:** Forward port `27017` from the `mongodb` service to your localhost.
<details>
  <summary><strong>Hint</strong>: Get all the resources inside the `mongodb` namespace</summary>

  ```
  kubectl port-forward svc/mongodb  27017:27017 -n mongodb 
  ```
</details>

After the completion of the port-forwarding you are able to insert the following conenction string in the MongoDB for VS Code extension: `mongodb://admin:password@127.0.0.1:27017`

**Task:** Establish the connection to MongoDB using the extension.

**Task:** Explore the playgrounds tab inside the extension. Click "Create New Playground" and execute the new playground.

**Task:** Explore the newly created database called `mongodbVSCodePlaygroundDB` and the inserted documents inside the `sales` collections. You should find the identical documents inside web interface [here](http://127.0.0.1:8084/db/mongodbVSCodePlaygroundDB/sales).


#### Exercise 4.1 - MongoDB and Kafka connect
create a connector whihc uses Kafka `INGESTION` topic as source and MongoDB as sik

```json
{
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
```

#### Exercise 4.2 - Query MongoBD

Create an query which filters the records of interest


[From Query API to your favorite language](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode)