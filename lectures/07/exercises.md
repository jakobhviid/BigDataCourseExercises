# Lecture 07 - Metadata, Data Provenance and Data Mesh

## Exercises

Please open issues [here](https://github.com/jakobhviid/BigDataCourseExercises/issues) if you encounter unclear information or experience bugs in our examples!

Before you start working on the exercises you are strongly encouraged to clean up your Kubernetes cluster. The exercises will assume you use the MicroK8s cluster on the provided virtual machines and that the cluster is in a "clean" state.

### Exercise 1 - 

[Deploying DataHub with Kubernetes](https://datahubproject.io/docs/deploy/kubernetes/)

```
k8s create namespace meta
```

```
kubectl -n meta create secret generic mysql-secrets --from-literal=mysql-root-password=datahubdatahub
kubectl -n meta create secret generic neo4j-secrets --from-literal=neo4j-password=datahubdatahub
```

```
helm repo add datahub https://helm.datahubproject.io/
```

```
helm install -n meta prerequisites datahub/datahub-prerequisites --values lectures/07/values.yaml
```

```
kubectl get pods -n meta -w  
```

```
helm install -n meta datahub datahub/datahub
```

```
kubectl get pods -n meta -w  
```

```
kubectl port-forward <datahub-frontend pod name> 9002:9002
```

- username: datahub
- password: datahub



### Exercise 2 - Organizing metadata


- As more metadata us added to Datahub the for



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

The Kafka Ingestion Source is not able to extract metadata on a topics key and values without setting up Kafka schemas. As this is not something we have touched upon, we will only set up a Kafka Ingestion source to extract topic names.

**Task:** Compose the stack in ./exercise07/docker-compose.yml to set up a simple Kafka cluster + Kowl. 

**Task:** Use the ingestion UI in Linkedin DataHub to create a Kafka Ingestion source that uses the Kafka
broker in the stack you just set up.

**Task:** Check that the ingestion worked, and you can see newly added topics in Linkedin DataHub.

>You can remove SSL authentication by going to the YAML view and deleting the lines related to SSL authentication.

> If you want to keep the stateful ingestion turned on (under advanced) you need to platform_instance = “somename” to your config. This can also be done in the YAML view.


### Exercise 5 - Add Linkedin DataHub’s internal MySQL database as an ingestion source
Linkedin DataHub creates a new MySQL database as part of its stack. We will try to add this database as an ingestion source for some data inception.



First screate a secret for the password



- The MySQL database has the following config:
    - host_port: prerequisites-mysql:3306
    - database: datahub
    - username: datahub
    - password: ${MySQL}


1. Set up a new MySQL Ingestion Source using the above config.

```yaml
source:
    type: mysql
    config:
        host_port: 'prerequisites-mysql:3306'
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