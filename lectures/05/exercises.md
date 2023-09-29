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

```
kubectl create namespace mongodb  
```

```
k8s apply -f mongodb.yaml -n mongodb       
```

```
kubectl port-forward svc/mongodb  27017:27017 -n mongodb 
```

```
mongodb://admin:password@127.0.0.1:27017
```

```
kubectl port-forward svc/mongo-express  8084:8084 -n mongodb
```


[MongoDB for VS Code](https://marketplace.visualstudio.com/items?itemName=mongodb.mongodb-vscode)

VS CODE extension for MongoDB as a client/editor for the data base?

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
