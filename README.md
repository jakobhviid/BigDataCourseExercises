# Big data and data science technologies course exercises
This repository contains the exercises related to the course [Big data and data science technologies](https://odin.sdu.dk/sitecore/index.php?a=fagbesk&id=81974&lang=en) at University of Southern Denmark.

## Instructors
This year instructors completed the course last year (E22) and will be facilitating and responsible for the exercises.  

Nicklas Marc Pedersen and Anders Launer Bæk-Petersen will be available on Discord channel for this course and any kind of feedback is more than welcome.

## Objective

The objective of the exercises is to navigate you through the practical aspects of the curriculum. The diagram below illustrates the technology stack and frameworks that will be used during this semester. 
We have this semester chosen to transition from a docker compose orchestrator to Kubernetes to minimize the gap between a single host system to a multi-node system. 

The diagram will be updated iteratively along with the progress of the course.


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
    subgraph Interactive containers
        ubuntupy(Python Data Scouce)
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

ubuntupy <--> namenode

end


```

## Virtual machines at SDU
Virtual machines will be available soon for this cource. 
Access to the portal can be found at [https://virtualresources.sdu.dk](https://virtualresources.sdu.dk) from the SDU local. Use VPN when home! 
Watch the video here to learn how virtual machines work: [SDU - Virtualresources](https://www.youtube.com/watch?v=iKM6P7nRzqI&feature=youtu.be).

## Content of the repository
The root of this repository will be related to the content of the current semester and the folder `archive` will contain material for the previous semester. The `lectures` folder and `services` folder contain the exercise material for the current semester. 

```
.
├── LICENSE
├── README.md
├── archive
│   └── E22
├── lectures
│   └── {01,02,03,...}
│       ├── exercises.md
│       └── ...
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
