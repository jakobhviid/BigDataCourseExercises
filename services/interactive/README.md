# Interactive containers

This folder contains components for creating a custom image that can be used to interact with HDFS by a Python client, to run other commands, and to create files using Visual Studio Code inside Kubernetes.  

The deployment manifest [`interactive.yaml`](./interactive.yaml) includes a pod definition for the interactive container and another resources used to claim persistent storage in Kubernetes.

The following cmd below can be used for creating a temporary instance of the image.
```
kubectl run interactive --rm -i --tty --image registry.gitlab.sdu.dk/jah/bigdatarepo/interactive:latest -- /bin/bash
```

## Attach Visual Studio Code to a running container
One convenient approach for making development inside Kubernetes is to attach Visual Studio Code to a running container. An introduction to this concept can be found here: [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers).   
You will need the following three extensions to make this work. All of them are developed by Microsoft. 

- [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
- [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Kubernetes](https://marketplace.visualstudio.com/items?itemName=ms-kubernetes-tools.vscode-kubernetes-tools)



A Kubernetes icon will appear in the activity bar after the installation of the mentioned extensions. The image below illustrates how to attach Visual Studio Code to the container.

![Attach to a container in a Kubernetes cluster](https://code.visualstudio.com/assets/docs/devcontainers/attach-container/k8s-attach.png)
*Image from [Attach to a container in a Kubernetes cluster. (Accessed: 09 September 2023)](https://code.visualstudio.com/assets/docs/devcontainers/attach-container/k8s-attach.png)*

This will open a new vscode window that is connected to the pod.