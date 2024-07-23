# Big Data and Data Science Technologies course exercises
This repository contains the exercises related to the course [Big Data and Data Science Technologies](https://odin.sdu.dk/sitecore/index.php?a=fagbesk&id=138236&listid=18888&lang=en) at University of Southern Denmark.

## Instructors
This year's instructors are Kasper Svane and Anders Launer Bæk-Petersen who completed the course in E23 and E22 respectively. We will facilitate the exercise hours and are available on the announced Discord channel for this course.
We encourage you to provide open and direct feedback along the semester. Please feel free to open new GitHub issues for bugs, etc..

## Objective
The objective of the exercises is to navigate you through the practical aspects of the curriculum. 
We chose to transition from the docker-compose orchestrator to Kubernetes to minimize the gap between a single host system to a multi-node system last semester (E23). Therfore our focus is to provide exercises whcih gives you hands-on experience with Kubernetes and the tools that are commonly used in the Big Data and Data Science field.

Our primary focus this semester is twofold:
- Fill in the missing gaps with extra exercises to match the curriculum for this course.  
- Streamline the existing exercises.

## Connect to the shared Kubernetes cluster

You will be using a shared Kubernetes cluster for the exercises hosted by the university. All the exercises are designed to be run from your localhost using `kubectl` commands.

You will be provided with a `kubeconfig` file that you can use to connect to the cluster prior to the first exercise session.
Information about the `kubeconfig` file(s) can be discoreved here: [Configure Access to Multiple Clusters](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/). For further information, please look into [Organizing Cluster Access Using kubeconfig Files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) if you need to manage multiple Kubernetes clusters in your own environment.

## Content of the repository
The root of this repository will be related to the content of the current semester and the folder `archive` will contain material for the previous semester. The `lectures` folder and `services` folder contain the exercise material for the current semester. 

```
.
├── LICENSE
├── README.md
├── archive
│   ├── E22 
│   └── E23
├── lectures
│   └── {01,02,03,...,07}
│       ├── ...
│       └── exercises.md
└── services
    ├── README.md
    ├── hdfs
    │   ├── ... 
    │   └── README.md
    ├── interactive
    │   ├── ...
    │   └── README.md
    └── kafka-connect
        ├── ...
        └── README.md
```
