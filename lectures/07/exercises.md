# Lecture 07 - Metadata, Data Provenance and Data Mesh
## DataHub Platform

The objevtive of these exercises is to play with a metadata platform which enable data provenance and supports the concepts of the Data Mesh paradigm. The platform of choise for this course is called DataHub and has been built by Acryl Data and LinkedIn. They promote their platform by the following verbs:

> "DataHub is an extensible metadata platform that enables data discovery, data observability and federated governance to help tame the complexity of your data ecosystem." - [DataHub landing page](https://datahubproject.io)

![DataHub Metadata Platform](https://datahubproject.io/assets/ideal-img/datahub-flow-diagram-light.5ce651b.1600.png)
*Image borrowed by [DataHub landing page](https://datahubproject.io)*.

## Exercises

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!

Before you start working on the exercises you are strongly encouraged to clean up your Kubernetes cluster. The exercises will assume you use the MicroK8s cluster on the provided virtual machines and that the cluster is in a "clean" state.

### Exercise 1 - Compose a DataHub Platform
This exercise will compose a DataHub platform which you will use in the up-comming exercises. We recommand to follow the steps in this exercise and use the two included value files [preq-values.yaml](preq-values.yaml) and [values.yaml](values.yaml) for the helm installation processes. The following steps have inspired by this guide [Deploying DataHub with Kubernetes](https://datahubproject.io/docs/deploy/kubernetes/). 

**Task: Add the helm repository for DataHub by running the following code.**

```
helm repo add DataHub https://helm.datahubproject.io/
```

**Task: Look into the [preq-values.yaml](preq-values.yaml) file and familize yourself with the four prerequisites components.**

DataHub is composed by four main components:
- DataHub metadata service (known as GMS). A service written in Java consisting of multiple servlets:
    - A public GraphQL API for fetching and mutating objects on the metadata graph.
    - A general-purpose Rest.li API for ingesting the underlying storage models composing the Metadata graph.
- Metadata audit event (known as MAE) consumer job. An optional component. Its main function is to listen to change log events emitted as a result of changes made to the Metadata Graph, converting changes in the metadata model into updates against secondary search & graph indexes (among other things). 
- Metadata Change Event (known as MCE) consumer job. An optional component. Its main function is to listen to change proposal events emitted by clients of DataHub which request changes to the Metadata Graph. It then applies these requests against DataHub's storage layer: the Metadata Service.
- DataHub frontend is a Play service written in Java. It is served as a mid-tier between DataHub GMS which is the backend service and DataHub Web.

**NB:** *Text in above bullets have been copied from [DataHub Metadata Service](https://datahubproject.io/docs/metadata-service), [Metadata Audit Event Consumer Job](https://datahubproject.io/docs/metadata-jobs/mae-consumer-job), [Metadata Change Event Consumer Job](https://datahubproject.io/docs/metadata-jobs/mce-consumer-job), [DataHub Frontend Proxy](https://datahubproject.io/docs/datahub-frontend) respectively.*

The main components are power by the following technoloiges:
- Kafka
- Local relational database: **MySQL**, Postgres, MariaDB
- Search Index: Elasticsearch
- Graph Index: **Neo4j** or Elasticsearch

**NB:** The technoloiges in **bold** have been chosen for these exercises.


introduction to preq-values.yaml, hvor kommer denne fra?


**Task: Create a namespace in Kubernetes called `meta`.** 

<details>
<summary><strong>Hint:</strong> Create namespace</summary>

```
k8s create namespace meta
```
</details>

**Task: Create two secrets called `mysql-secrets` and `neo4j-secrets` in Kubernetes with the following values.** 

- secret name: `mysql-secrets`
    - field: `mysql-root-password` = `datahubdatahub`
    - field: `mysql-username` = `root`
- secret name: `neo4j-secrets`
    - field: `neo4j-password` = `datahubdatahub`
    - field: `neo4j-username` = `neo4j`
    - field: `NEO4J_AUTH` = `neo4j/datahubdatahub`


<details>
<summary><strong>Hint:</strong> Create secrets in Kubernetes.</summary>

Run the following two cmd's

```
kubectl -n meta create secret generic mysql-secrets --from-literal=mysql-root-password=datahubdatahub --from-literal=mysql-username=root
```
```
kubectl -n meta create secret generic neo4j-secrets --from-literal=neo4j-password=datahubdatahub --from-literal=neo4j-username=neo4j --from-literal=NEO4J_AUTH=neo4j/datahubdatahub
```
</details>


**Task: Add the DataHub helm repository by running: `helm repo add DataHub https://helm.datahubproject.io/`** 


**Task: Deploy the four main components to power the DataHub platform.**

Execute the following cmd: `helm install -n meta preq datahub/datahub-prerequisites --values preq-values.yaml`

**NB:** This may take several minutes. To keep track of the progress you can either run `kubectl get pods -n meta -w` or an alterantive cmd like `watch -n1 kubectl get pods -n meta` in a secondary terminal session. The latter requries an `watch` executable on your localhost.


**Task: Deploy the DataHub platform.**

Execute the following cmd: `helm install -n meta datahub datahub/DataHub --values values.yaml`

**NB:** This may take several minutes. To keep track of the progress you can either run `kubectl get pods -n meta -w` or an alterantive cmd like `watch -n1 kubectl get pods -n meta` in a secondary terminal session. 


**Task: Clean up completed and possible failed pods.**

<details>
<summary><strong>Hint:</strong> Identify pods and delete using a field selector in Kubernetes.</summary>

The first chunk will list pods which state is either `Succeeded` or `Failed`. 
```
kubectl -n meta get pod --field-selector=status.phase==Succeeded,status.phase==Failed
```
The secound chunk will delete pods which state is either `Succeeded` or `Failed`. 
```
kubectl -n meta delete pod --field-selector=status.phase==Succeeded,status.phase==Failed
```
</details>

**Task: Validate the MySQL database is running.**

Steps:
1. Set up port-forwarding: `kubectl -n meta port-forward svc/preq-mysql 3306:3306`
1. Connect to the MySQL database with your favorite editor.
    - Host: `127.0.0.1`
    - Port: `3306`
    - User: `mysql-username` created in the secret: `mysql-secrets`
    - Password: `mysql-root-password` created in the secret: `mysql-secrets`
    - Database: `datahub`
1. Once you connect there should be a table called `metadata_aspect_v2` in the `datahub` MySQL database.


**Task: Validate the frontend is running.**

Steps:
1. Set up port-forwarding: `kubectl -n meta port-forward svc/datahub-datahub-frontend 9002:9002`
1. Connect to the fronted [localhost:9002](http://localhost:9002).
1. Once you connect you should be able to login with:
    - Username: datahub
    - Password: datahub



### Exercise 2 - Organizing metadata


- As more metadata us added to DataHub the for



**Task:** Play around in the UI, and see if you can add the following: 
1. A new domain
1. A new Glossary Group
    - Add 1-2 new glossaries in your new Glossary Group.
1. One new glossary that inherits from another glossary.

**Task:** Now try and use your glossaries on some of the existing dummy data.

**Task:** What metadata does a glossary term that is inherited by another term show? Can you explain this?

### Exercise 3 - Checkout analytics!
DataHub comes with a nice analytics overview. Here we can gain an overview of how the platform is used.

**Task:** Play around in the Analytics UI.

**Task:** Can you find analytics for your newly added Domain?


### Exercise 4 - Add a Kafka Ingestion Source

We will now create an Ingestion source for a Kafka cluster. An ingestion source tells DataHub how to connect to a service and allows DataHub to collect metadata from it. In the case of Kafka, it collects topic names, and if you are using for example Avro, then it can collect information about the schema from the schema registry.

If you don't have a Kafka cluster already then create one.

**Task:** Create a Kafka cluster and also deploy Redpanda

**Hint:** Go back to [lecture 3 exercise 1](../03/exercises.md#exercise-1---composing-a-kafka-cluster)

Now that you have a Kafka cluster deployed, you can then add it as an ingestion source.

**Task:** Create an ingestion source for the Kafka cluster

Once you have created the ingestion source it will then run. Make sure that the run is succeeded. If not then you can check the logs to figure out the problem.

**Task:** Check that the ingestion worked

If the ingestion worked then you should see Kafka as a platform on the start page of Datahub.

**Task:** Look at the Kafka platform

You may or may not see any topcs for Kafka on Datahub. If there are no topics, then it is because your Kafka cluster has no topics. Try to create a topic.

**Task:** Create a Kafka topic

Now that you have created a topic you can then try to check if it is available on Datahub. But you should see that nothing has changed. This is because DataHub pulls metadata on configured intervals. But you can manually trigger the ingestion source.

**Task:** Manually trigger the ingestion source

When it is done running, you can then look for the topic you created and you should see it inside Datahub. You can now document the topic, add tags and terms etc.

### Exercise 5 - Add Linkedin DataHub’s internal MySQL database as an ingestion source
Linkedin DataHub creates a new MySQL database as part of its stack. We will try to add this database as an ingestion source for some data inception.



First screate a secret for the password



- The MySQL database has the following config:
    - host_port: preq-mysql:3306
    - database: datahub
    - username: datahub
    - password: ${MySQL}


1. Set up a new MySQL Ingestion Source using the above config.

```yaml
source:
    type: mysql
    config:
        host_port: 'preq-mysql:3306'
        database: null
        username: root
        include_tables: true
        include_views: true
        profiling:
            enabled: true
            profile_table_level_only: true
        stateful_ingestion:
            enabled: true
        password: '${MySQL}'
```

1. Check out your new metadata entities. Can you spot some of the niceties that come with enabling profiling?

**Note:** Profiling: enabled: true # this allows the ingestion source to collect metadata on e.g. sample data and other niceties.


### Exercise 6 - Alice in Metaverse Part 1 👸
Your task is to create a new table in the database "datahub" and ingest all the words from Alice in Wonderland!

#### Exercise 6.1 - 👸
1. Create a new database called "alice"
1. Read alice-in-wonderland.txt
1. Upload the individual words to the table

Look at datahub, and see what changed and what you can see about alice in datahub!
**Note:** May need to sync manually.

#### Exercise 6.2 - 👸

CREATE VIEW alice_agg AS SELECT word, COUNT(*) as n FROM alice GROUP BY word;
**Note:** May need to sync manually.

#### Exercise 6.2 - Check linage

Is it missing, how can be create linage??

https://datahubproject.io/docs/api/tutorials/lineage/


```python
# Inlined from /metadata-ingestion/examples/library/lineage_emitter_rest.py
import datahub.emitter.mce_builder as builder
from datahub.emitter.rest_emitter import DatahubRestEmitter

# Construct a lineage object.
lineage_mce = builder.make_lineage_mce(
    [
        builder.make_dataset_urn("hive", "fct_users_deleted"),  # Upstream
    ],
    builder.make_dataset_urn("hive", "logging_events"),  # Downstream
)

# Create an emitter to the GMS REST API.
emitter = DatahubRestEmitter("http://localhost:8080")

# Emit metadata!
emitter.emit_mce(lineage_mce)
```


**Note:** May need to sync manually.





## Clean up 


```
helm uninstall -n meta datahub
helm uninstall -n meta preq

kubectl -n meta delete secret mysql-secrets
kubectl -n meta delete secret neo4j-secrets

k8s delete namespace meta
```