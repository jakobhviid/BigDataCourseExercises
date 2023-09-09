# Interactive containers

This folder contains components for creating a custom image that can be used to interact with HDFS by a Python client.  

The deployment manifest `anbae-big-data-course.yaml` includes a pod definition for the interactive container and two other resources used to claim persistent storage in Kubernetes.

The following cmd below can be used for creating a temporary instance of the image.
```
kubectl run anbae --rm -i --tty --image anderslaunerbaek/anbae-big-data-course:latest -- bash
```

## Attach VS Code to a running container
One convenient approach for making development inside Kubernetes is to attach VS Code to a running container.  
You will need the following three extensions to make this work and all of them are developed by Microsoft.
- Remote Development
- Dev Containers
- Kubernetes
Introduction to this concept can be found here: [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers). 


A Kubernetes icon will appear in the activity bar after the installation of the mentioned extensions. The image below illustrates how to attach to VS Code to the container.

![Attach to a container in a Kubernetes cluster](https://code.visualstudio.com/assets/docs/devcontainers/attach-container/k8s-attach.png)
*Image from [Attach to a container in a Kubernetes cluster. (Accessed: 09 September 2023)](https://code.visualstudio.com/assets/docs/devcontainers/attach-container/k8s-attach.png)*

