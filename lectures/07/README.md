# Lecture 07 - Metadata, Data Provenance and Data Mesh

## DataHub Platform

The objective of these exercises is to play with a metadata platform that enables data provenance and supports the concepts of the Data Mesh paradigm. The platform of choice for this course is called DataHub and has been built by Acryl Data and LinkedIn. They promote their platform by the following verbs:

> "DataHub is an extensible metadata platform that enables data discovery, data observability and federated governance to help tame the complexity of your data ecosystem." - [DataHub landing page](https://datahubproject.io)

![DataHub Metadata Platform](https://datahubproject.io/assets/ideal-img/datahub-flow-diagram-light.5ce651b.1600.png)
*Image borrowed by [DataHub landing page](https://datahubproject.io)*.

## Exercises

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!

Before you start working on the exercises you are strongly encouraged to clean up your Kubernetes cluster. The exercises will assume you use the MicroK8s cluster on the provided virtual machines and that the cluster is in a "clean" state.

### Exercise 1 - Compose a DataHub Platform

This exercise will compose a DataHub platform which you will use in the upcoming exercises. We recommend following the steps in this exercise and using the two included value files [preq-values.yaml](preq-values.yaml) and [values.yaml](values.yaml) for the helm installation processes. The following steps have been inspired by this guide [Deploying DataHub with Kubernetes](https://datahubproject.io/docs/deploy/kubernetes/).

**Task: Add the helm repository for DataHub by running the following command.**

```
helm repo add datahub https://helm.datahubproject.io/
```

**Task: Look into the [preq-values.yaml](preq-values.yaml) file and familize yourself with the four prerequisites components.**

DataHub is composed by four main components:
- DataHub metadata service (known as GMS). A service written in Java consisting of multiple servlets:
    - A public GraphQL API for fetching and mutating objects on the metadata graph.
    - A general-purpose Rest.li API for ingesting the underlying storage models composing the Metadata graph.
- Metadata audit event (known as MAE) consumer job. An optional component. Its main function is to listen to change log events emitted as a result of changes made to the Metadata Graph, converting changes in the metadata model into updates against secondary search & graph indexes (among other things).
- Metadata Change Event (known as MCE) consumer job. An optional component. Its main function is to listen to change proposal events emitted by clients of DataHub which request changes to the Metadata Graph. It then applies these requests against DataHub's storage layer: the Metadata Service.
- DataHub frontend is a Play service written in Java. It is served as a mid-tier between DataHub GMS which is the backend service and DataHub Web.

**Note:** *Text in above bullets have been copied from [DataHub Metadata Service](https://datahubproject.io/docs/metadata-service), [Metadata Audit Event Consumer Job](https://datahubproject.io/docs/metadata-jobs/mae-consumer-job), [Metadata Change Event Consumer Job](https://datahubproject.io/docs/metadata-jobs/mce-consumer-job), [DataHub Frontend Proxy](https://datahubproject.io/docs/datahub-frontend) respectively.*

The main components are power by the following technoloiges:
- Kafka
- Local relational database: **MySQL**, Postgres, MariaDB
- Search Index: Elasticsearch
- Graph Index: **Neo4j** or Elasticsearch

**Note:** The technologies in **bold** have been chosen for these exercises.

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

Run the following two cmd's:

```
kubectl create secret generic mysql-secrets --from-literal=mysql-root-password=datahubdatahub --from-literal=mysql-username=root
```
```
kubectl create secret generic neo4j-secrets --from-literal=neo4j-password=datahubdatahub --from-literal=neo4j-username=neo4j --from-literal=NEO4J_AUTH=neo4j/datahubdatahub
```
</details>


**Task: Add the DataHub helm repository by running: `helm repo add datahub https://helm.datahubproject.io/`**


**Task: Deploy the four main components to power the DataHub platform.**

Execute the following cmd: `helm install preq datahub/datahub-prerequisites --values preq-values.yaml`

**Note:** This may take several minutes. To keep track of the progress you can either run `kubectl get pods -w` or an alternative cmd like `watch -n1 kubectl get pods` in a secondary terminal session. The latter requires an `watch` executable on your localhost.


**Task: Deploy the DataHub platform.**

Execute the following cmd: `helm install datahub datahub/datahub --values values.yaml`

**Note:** This may take several minutes. To keep track of the progress you can either run `kubectl get pods -w` or an alternative cmd like `watch -n1 kubectl get pods` in a secondary terminal session.


**Task: Clean up completed and possible failed pods.**

<details>
<summary><strong>Hint:</strong> Identify pods and delete using a field selector in Kubernetes.</summary>

The first chunk will list pods that state are either `Succeeded` or `Failed`.
```
kubectl get pod --field-selector=status.phase==Succeeded,status.phase==Failed
```
The secound chunk will delete pods that state are either `Succeeded` or `Failed`.
```
kubectl delete pod --field-selector=status.phase==Succeeded,status.phase==Failed
```
</details>

**Task: Validate the MySQL database is running.**

Steps:
1. Set up port-forwarding: `kubectl port-forward svc/preq-mysql 3306:3306`
1. Connect to the MySQL database with your favorite editor.
    - Host: `127.0.0.1`
    - Port: `3306`
    - User: `mysql-username` created in the secret: `mysql-secrets`
    - Password: `mysql-root-password` created in the secret: `mysql-secrets`
    - Database: `datahub`
1. Once you connect there should be a table called `metadata_aspect_v2` in the `datahub` MySQL database.


**Task: Validate the frontend is running.**

Steps:
1. Set up port-forwarding: `kubectl port-forward svc/datahub-datahub-frontend 9002:9002`
1. Connect to the fronted [localhost:9002](http://localhost:9002).
1. Once you connect you should be able to login with:
    - Username: datahub
    - Password: datahub



### Exercise 2 - Organizing metadata

The importance of organizing the metadata of the data sources has a direct impact on the usability of the platform. To master the metadata of the data sources need to talk about three components; domains, business glossary, and tags.

- **Domains** are collections of related data assets associated with a specific part of your organization, such as the Marketing department. Get a further explanation of domains in DataHub [here](https://datahubproject.io/docs/domains/).
- **Business glossary** can organize data assets using a shared vocabulary. The glossaries provide a framework for defining a standardized set of data concepts and then associating them with the physical assets that exist within your data ecosystem. Get a further explanation of the business glossary in DataHub [here](https://datahubproject.io/docs/glossary/business-glossary).
- **Tags** are also useful for organizing metadata, but there is not a strict policy on how to use them. They can be used to e.g. add versioning to an entity, or whether an entity is a legacy and to classify the several environments data assets can live in. Get a further explanation on tags in DataHub [here](https://datahubproject.io/docs/tags).


**Task: Login to the [frontend](http://localhost:9002) and play around in the UI.**

**Task: Create your glossary terms with the UI.**

1. A new domain that reflects the part of the organization you are interested in. E.g. `Engineering`.
1. A new business glossary term group. E.g. `RD`.
1. Append two terms in your newly created term group (`RD`) called `experiments` and `results`.
1. Hereafter create one new term (`analysis`) that inherits from the `RD` term group. How do you expect `analysis` will fit in the hierarchy?

**Hint:** Watch this short session [DataHub 201: Business Glossary](https://youtu.be/pl9zx0CtdiU?si=1JLSC0C5uD7pOth2) on youtube to get a different explanation on this concept.

**Task: BONUS: Create the same glossary terms in a yaml file.**

**Note:** A solution for this exercise is all yours! However, it is important to state that this method enables version control - which all of us prefer!

**Hint:** [GitHub: datahub/metadata-ingestion/examples/bootstrap_data/business_glossary.yml](https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/examples/bootstrap_data/business_glossary.yml)

### Exercise 3 - Checkout analytics overview in the UI
The DataHub platform comes with a nice analytics overview page. Navigate to [localhost:9002/analytics](http://localhost:9002/analytics).
Here we can obtain an overview of the usage of the platform and various other statistics.

**Task: Play around in the Analytics UI.**

- What do see?

**Task: Find metics for your newly added Domain.**

- Filter "Data Landscape Summary" to only include the `Engineering` domain and report the "Section Views across Entity Types" metrics to rest of the project group.

### Exercise 4 - Add a Kafka ingestion source

We will now create an Ingestion source for a Kafka cluster.
An ingestion source tells DataHub how to connect to a service and allows DataHub to collect metadata from the service. In the case of a given Kafka cluster, DataHub is collecting topic names. The DataHub platform can collect information about the record schema from a schema registry service. This is recommanded if you are using the Avro file format for the records in the topics.

**Note:** We are not using schema registry for this exercise session.

**Task: Create a Kafka cluster and also deploy Redpanda.**

**Hint:** Go back to [lecture 3 exercise 1](../03/exercises.md#exercise-1---composing-a-kafka-cluster) and deploy a Kafka cluster.

Once your Kafka cluster has been deployed, you can then add the cluster as an ingestion source in the DataHub platform.

**Note:** If you experience an error code like `429 Too Many Requests` during the deployment we can use the Kafka cluster deployed by the DataHub platform instead.

**Task: Create an ingestion source for the Kafka cluster.**

1. Navigate to [localhost:9002/ingestion](http://localhost:9002/ingestion).
1. Click on "Create new source"
    1. Choose type: `Kafka`.
    1. Configure recipe:
        1. Fill the field of Bootstrap Servers:
            - `preq-kafka:9092` using the internal Kafka cluster in the DataHub plarform
            - `strimzi-kafka-bootstrap.kafka:9092` if you will you the approach from [lecture 3 exercise 1](../03/exercises.md#exercise-1---composing-a-kafka-cluster).
        1. Enable stateful ingestion under the advaced settings.
        1. This will end up in a similar configuration as below:
            ```yaml
            source:
            type: kafka
            config:
                connection:
                    consumer_config:
                        security.protocol: PLAINTEXT
                    bootstrap: 'preq-kafka:9092'
                stateful_ingestion:
                    enabled: true

            ```
    1. Schedule Ingestion: Toggle "Run on a schedule"
    1. Finish up: Provide a name (`Kafka`) for your ingestion source.
1. Once you have created the ingestion source it will then run. Make sure that the run is succeeded. If not then you can check the logs to figure out the problem.

**Task: Check that the ingestion worked.**

1. Navigate to [localhost:9002](http://localhost:9002).
1. If the ingestion worked then you should see platform named Kafka on the landing page of Datahub.

**Task: Look at the Kafka platform.**

You may or may not see any topcs for Kafka on Datahub. If there are no topics, then it is because your Kafka cluster has no topics. Try to create a topic.

**Task: Create a Kafka topic (Optional).**

Now that you have created a topic you can then try to check if it is available on Datahub. However, you should see that nothing has changed. This is because DataHub pulls metadata on configured intervals.

**Task: Manually trigger the ingestion source.**

You can manually trigger the ingestion source here [localhost:9002/ingestion](http://localhost:9002/ingestion).
When it is done, you can look for the your newly created topic and this topic should be explorable in Datahub.

**Task: Enrich the metadata for a Kafka topic.**

1. Select a given topic.
1. Update the metadata fields for the given topic. If the current tags, terms, domains etc. is not suffienct. Then add additional tags, terms and domains to represent the given topic.
    - About
    - Owners
    - Tags
    - Glossary Terms
    - Domain


### Exercise 5 - Add a MySQL database as ingestion source
This exercise is about adding a secondary ingestion source. The source is an already existing MySQL database.

**Task: Create an ingestion source for the MySQL databse cluster.**

1. Navigate to [localhost:9002/ingestion](http://localhost:9002/ingestion).
1. Create a secret for the database password. Click on "Create new srecet" in the Secrets tab.
    1. Provide a name: `pw-mysl-db`
    1. Provide the database password generated in [Exercise 1](#exercise-1---compose-a-datahub-platform).
    1. Click Create.
1. Click on "Create new source" in the Sources tab.
    1. Choose type: `MySQL`.
    1. Configure recipe:
        1. Host and Port: `preq-mysql:3306`
        1. Username: `root`
        1. Password: `${pw-mysl-db}`
        1. Add a database allowance filter: `datahub`
        1. This will end up in a similar configuration as below:
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
                    password: '${pwmysqldb}'
                    database_pattern:
                        allow:
                            - datahub

            ```
    1. Schedule Ingestion: Toggle "Run on a schedule"
    1. Finish up: Provide a name (`MySQL`) for your ingestion source.
1. Once you have created the ingestion source it will then run. Make sure that the run is succeeded. If not then you can check the logs to figure out the problem.

### Exercise 6 - Adding a custom dataset to DataHub
The objective of this exercise is to add a custom dataset to DataHub. The exercise consists of an already complete example. However, you are more than welcome to modify the existing example to fit your selected project.

The example is about tracking experiments. In this case, a simple experiment where a random value will be drawn multiple times from a uniform distribution between 0 and 1. The results of the experiments will be stored in a database composed of two tables in a database called `experiment` and `results` and a view called `analysis`. Moreover, a Python script ([hints/experiment.py](./hints/experiment.py)) has been provided to simulate multiple new experiments.

#### Exercise 6.1 - Simulate experiments
Decide whether to go with the existing example or modify and create your content to match to project.

**Task: Familiarize your self with [hints/experiment.py](./hints/experiment.py) Python file.**
- Which framework is used to interact with the databse?

**Task: Denote the schemas for the `experiment` and `results` tables in the database.**

**Task: Execute the [hints/experiment.py](./hints/experiment.py) Python file.**

**Note:** This task assumes you already have access to the database from your localhost. If not please enable the port-forwarding: `kubectl port-forward svc/preq-mysql 3306:3306`.


**Task: Create an `analysis` view in the database to summarise the experiments.**
- Use the SQL statement below:
    ```sql
    CREATE VIEW analysis AS SELECT r.experiment_id, e.created_date, r.valid, AVG(r.value) avg_value FROM results r INNER JOIN experiment e ON r.experiment_id=e.id GROUP BY r.experiment_id, r.valid;
    ```

**Task: What are the average value of from the simulated experiments?**

#### Exercise 6.2 - Data discovery and rich metadata on the newly create tables

[Exercise 6.1](#exercise-61---Simulate-experiments) uses the internal database deployed by DataHub to store the results of the experiments.

**Task: Navigate to [localhost:9002/ingestion](http://localhost:9002/ingestion) and run ingestion on the MySQL platform.**

**Task: Validate the three newly created datasets in the MySQL platform.**

**Hint:** Nagivate to [http://localhost:9002/search?filter_platform=urn:li:dataPlatform:mysql](http://localhost:9002/search?filter_platform=urn:li:dataPlatform:mysql)

**Task: Update metadata to the three newly created datasets.**

- Datasets of interest:
    - [Table/MySQL/datahub/experiment](http://localhost:9002/dataset/urn:li:dataset:(urn:li:dataPlatform:mysql,datahub.experiment,PROD)/Schema?is_lineage_mode=false&schemaFilter=)
    - [Table/MySQL/datahub/results](http://localhost:9002/dataset/urn:li:dataset:(urn:li:dataPlatform:mysql,datahub.results,PROD)/Schema?is_lineage_mode=false&schemaFilter=)
    - [View/MySQL/datahub/analysis](http://localhost:9002/dataset/urn:li:dataset:(urn:li:dataPlatform:mysql,datahub.analysis,PROD)/Schema?is_lineage_mode=false&schemaFilter=)
- Metadata of interest:
    - Owner
    - Tags
    - Glossary Terms
    - Domain

#### Exercise 6.3 - Enable data provenance
Data provenance is important in analytical applications to understand underlying dependencies. The objective of this sub-exercise is to update the lineage between the three newly created datasets.

This exercise is motivated and inspired by [About DataHub Lineage](https://datahubproject.io/docs/lineage/lineage-feature-guide/) and [Lineage - Why Would You Use Lineage?](https://datahubproject.io/docs/api/tutorials/lineage/). There is a Python file here: [hints/linage.py](./hints/linage.py) which updates the lineage between the three datasets.

**Task: Familiarize yourself with [hints/lineage.py](./hints/lineage.py) Python file.**

**Task: Execute the [hints/lineage.py](./hints/lineage.py) Python file.**

**Note:** This task assumes you already have access to Datahub GMS from your localhost. If not please enable the port-forwarding: `kubectl port-forward svc/datahub-datahub-gms 8080:8080`.

**Task: Navigate to [View/MySQL/datahub/analysis - lineage](http://localhost:9002/dataset/urn:li:dataset:(urn:li:dataPlatform:mysql,datahub.analysis,PROD)/Schema?end_time_millis&is_lineage_mode=true&schemaFilter=&start_time_millis) and identify the two upstram datasets.**

**Task: Navigate to [View/MySQL/datahub/analysis - lineage](http://localhost:9002/dataset/urn:li:dataset:(urn:li:dataPlatform:mysql,datahub.analysis,PROD)/Schema?end_time_millis&is_lineage_mode=true&schemaFilter=&start_time_millis) and take a screenshot.**


#### Exercise 6.4 - Data provenance as a data expert evangelist

We are now interested in updating to column-level lineage from the general lineage ([Exercise 6.3](#exercise-63---enable-data-provenance)).

**Task: Look into the example of column-level lineage [here](https://datahubproject.io/docs/api/tutorials/lineage/#add-column-level-lineage).**

**Task: Create a new Python file which encounter for column-level lineage.**

**Hint: You may look into [Exercise 6.1](#exercise-61---Simulate-experiments) and examene the `analyis` view to understand the lineage bewteen the three datasets.**

## Clean up - So far so good. 💪🏼
You are able to clean up your environment by running the commands in the chunk below:

```
helm uninstall datahub
helm uninstall preq

kubectl delete namespace meta
```
