# Lecture 02 - HFDS and different file formats

## GENERAL
WIP: Create and issue on github if you encountering errors




## Subject and objective for these exercises

## Exercises

### Exercise 1 - Composing a HDFS Cluster

- To work with HDFS we need to setup a HDFS cluster.
- Questions:
  -  

### Exercise 2 - Accessing the namenode and interacting with the HDFS CLI

Now that we have a HDFS cluster, lets try and access a node, and play around. 
- To access the HDFS cluster do the following: TODO: update cmd -> `docker exec -ti namenode /bin/bash`

Now we have access to the namenode container that is able to interact with the HDFS CLI. 
Now lets try to run some HDFS shell commands:

- We will use the `hdfs dfs -[command] [path]` command
  - `hdfs dfs -ls [path]` to list all files in a specified folder.
  - `hdfs dfs -cat [path]` to print the contents of a file on a specific path.
  - `hdfs dfs -put [sourcePath] [targetPath]` to add a file to hdfs. The source path points to a file inside the container, and the target path should point to a path inside hdfs.

You might want to create a file first:
  - Create file: `echo "Hello world" > hello-world.txt` 
  - Put into HDFS: `hdfs dfs -put hello-world.txt /lecture02/` 

### Exercise 3 - Access txt data on HDFS from a Python client (Read and write)

Now we want to access HDFS from a client. To do this we will create a Python client that can read and write to HDFS.

TODO: Interactive session
complete `simple-client.py`


### Exercise 4 - Create JSON data to HDFS from a Python client


Now that we have a python client that can write from HDFS. We can try to write JSON from HDFS.
TODO: Interactive session
complete `counting-json.py`

Questions:
- What are the five most common words in TODO?? Alice in Wonderland, and how many times are they repeated?

### Exercise 5 - Create avro data to HDFS from a Python client


Now that we have a python client that can write from HDFS. we can try to write JSON from HDFS.
TODO: Interactive session
complete `counting-avro.py`

Questions:
- What are the five least common words in TODO?? Alice in Wonderland, and how many times are they repeated?

### Exercise 6 - Create parquet data to HDFS from a Python client


Now that we have a python client that can write from HDFS. we can try to write JSON from HDFS.
TODO: Interactive session
complete `counting-parquet.py`

Questions:
- What is the schema??
- Hvordan vil tabellen se ud med i bred format?


### Exercise 7 - Create six fictive data sources

Simulate multiple data streams from an identical sensor with a sample frequency of 1hz placed a six different locations. 

- You need to find a proper directory pattern to store these samples in HDFS for later analysis
- Which file format do we prefer?
- The schema of a sample may be similar to:
```json

{
    "payload": {
        "station_id": "1", // value in <"1", "2", "2", "3", "4", "5">
        "modality": 11.0, // value between 0 and 600
        "unit": "MW", // unit
        "temporal_aspect":"real_time", // value in <"real_time", "edge_prediction">
    },
    "correlation_id": "23c4d380-b357-4082-9298-314ba9ef1b68", // correlation uuid for this sample
    "created_at": 1667205100.786588, // UNIX time
    "schema_version": 1
}
```
- write a data producer for simulating these six sensors and use of the python client logic to write files into HDFS


Questions:
- What is the schema??
- What is the proper folder structure inside HDFS?
- 