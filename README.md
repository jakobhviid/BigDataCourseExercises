# Big data and data science technologies course exercises
This repository contains the exercises related to the course [Big data and data science technologies](https://odin.sdu.dk/sitecore/index.php?a=fagbesk&id=81974&lang=en) at University of Southern Denmark.


## Objective

WIP

```mermaid
graph

subgraph Kubernetes
    subgraph Storage 
    
        subgraph HDFS
            namenode(NameNode)
            datanode01(DataNode 01)
            datanode02(DataNode 02)
            datanode03(DataNode 03)
            namenode <--> datanode01 & datanode02 & datanode03
        end
        registry(Kafka registry)
    end

    subgraph Transportation
        transkafka(Kafka)
        transconnect(Kafka connect)
        transspark(Spark structured streaming)
    end
    
    subgraph Querying
        subgraph Hive
        end
        queryksqldb(ksqlDB)
    end
    
    
    subgraph Processing
        processksqldb(ksqlDB)
        processspark(Spark)
    end


    subgraph UI
        uiconcontrol(Confluent control)
        uidatahub(Datahub)
    end

end


```

## Content of the repository
The root of this repository will be related to the content of the current semester and the folder `archive` will contain material for the previous semester.

```
.
├── LICENSE
├── README.md
├── archive
│   └── E22
├── lectures
│   └── {01,02,03,...}
│       ├── README.md
│       └── content
│           └── {01,02,03,...}-exercise.md
└── services
    ├── README.md
    ├── datahub
    │   └── README.md
    ├── hdfs
    │   └── README.md
    ├── hive
    │   └── README.md
    ├── kafka
    │   └── README.md
    └── spark
        └── README.md
```