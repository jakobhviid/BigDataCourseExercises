# Lecture 01 - Kubernetes fundaments

## Introduction to the instructors

### Nicklas Marc Pedersen
WIP

### Anders Launer Bæk-Petersen

![Anders Launer Bæk-Petersen](https://avatars.githubusercontent.com/u/28479232?v=4)
- PhD Fellow ~ Center for Energy Informatics University of Southern Denmark
    - Transferable AI Model Development Framework for Smart Energy Systems
- Instustry for 4,5 years, 
    - Machine Learning Engineer ~ Energinet
    - Data Scientist ~ Esoft R&D
    - Research Assistant ~ Technical University of Denmark
- Master of Science in Mathematical Modelling and Computation ~ Technical University of Denmark 
- Bachlor of Science in Robot Systems ~ University of Southern Denmark 
- LinkedIn ~ [linkedin.com/in/anderslaunerbaek](https://www.linkedin.com/in/anderslaunerbaek/)

## Subject and objective for these exercises

The exercises for the first lecture is to introduce and refresh the nesseary components and terminology of Kubernetes. The below mentioned material have been sourced from [https://kubernetes.io/docs/tutorials/kubernetes-basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/) and familizing with this content will be suffienct for progressing along the exercises. 


## Brief introduction to Kubernetes
WIP 

### [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

WIP


![Kubernetes Cluster](https://d33wubrfki0l68.cloudfront.net/283cc20bb49089cb2ca54d51b4ac27720c1a7902/34424/docs/tutorials/kubernetes-basics/public/images/module_01_cluster.svg)
*Image from [kubernetes.io - Cluster Diagram. (Accessed: 04 September 2023)](https://d33wubrfki0l68.cloudfront.net/283cc20bb49089cb2ca54d51b4ac27720c1a7902/34424/docs/tutorials/kubernetes-basics/public/images/module_01_cluster.svg)*

### [Using kubectl to Create a Deployment](https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/)

WIP

![ Deploying your first app on Kubernetes](https://d33wubrfki0l68.cloudfront.net/8700a7f5f0008913aa6c25a1b26c08461e4947c7/cfc2c/docs/tutorials/kubernetes-basics/public/images/module_02_first_app.svg)
*Image from [kubernetes.io - Deploying your first app on Kubernetes. (Accessed: 04 September 2023)](https://d33wubrfki0l68.cloudfront.net/8700a7f5f0008913aa6c25a1b26c08461e4947c7/cfc2c/docs/tutorials/kubernetes-basics/public/images/module_02_first_app.svg)*

### [Viewing Pods and Nodes](https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/)
WIP
#### Pods
WIP
![Pods overview](https://d33wubrfki0l68.cloudfront.net/fe03f68d8ede9815184852ca2a4fd30325e5d15a/98064/docs/tutorials/kubernetes-basics/public/images/module_03_pods.svg)
*Image from [kubernetes.io - Pods overview. (Accessed: 04 September 2023)](https://d33wubrfki0l68.cloudfront.net/fe03f68d8ede9815184852ca2a4fd30325e5d15a/98064/docs/tutorials/kubernetes-basics/public/images/module_03_pods.svg)*

#### Nodes
WIP
![Node overview](https://d33wubrfki0l68.cloudfront.net/5cb72d407cbe2755e581b6de757e0d81760d5b86/a9df9/docs/tutorials/kubernetes-basics/public/images/module_03_nodes.svg)
*Image from [kubernetes.io - Node overview. (Accessed: 04 September 2023)](https://d33wubrfki0l68.cloudfront.net/5cb72d407cbe2755e581b6de757e0d81760d5b86/a9df9/docs/tutorials/kubernetes-basics/public/images/module_03_nodes.svg)*


#### Troubleshooting with kubectl
- `kubectl get` - list resources
- `kubectl describe` - show detailed information about a resource
- `kubectl logs <contianer name>` - print the logs from a container in a pod
- `kubectl exec <contianer name>` - execute a command on a container in a pod

### [Using a Service to Expose Your App](https://kubernetes.io/docs/tutorials/kubernetes-basics/expose/expose-intro/)
WIP
![Services and Labels](https://d33wubrfki0l68.cloudfront.net/7a13fe12acc9ea0728460c482c67e0eb31ff5303/2c8a7/docs/tutorials/kubernetes-basics/public/images/module_04_labels.svg)
*Image from [kubernetes.io - Services and Labels. (Accessed: 04 September 2023)](https://d33wubrfki0l68.cloudfront.net/7a13fe12acc9ea0728460c482c67e0eb31ff5303/2c8a7/docs/tutorials/kubernetes-basics/public/images/module_04_labels.svg)*


## Exercises
### Exercise 01 - Setup your Kubernetes environment
```
kubectl get
```
### Exercise 02 - Deploy your "Hello World" application
Node.js hello world 

write yml deployment file
```
kubectl apply -f <file name>
```
### Exercise 03 - Validate your deployment
```
kubectl xyz
```
### Exercise 04 - Expose your "Hello World" application
write yml service file
```
kubectl apply -f <file name>
```
### Exercise 05 - Scale your application 

manually
```
kubectl scale deployments/<name of deployment> --replicas=<x>
```

update deployment


### Exercise 06 - Remove deployment of your "Hello World" application