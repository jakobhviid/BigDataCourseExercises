# Virtual Machines at SDU

SDU is hosting virtual machines (VMs) for your Big Data and Data Science Technology project. 
Each project group have access to three VMs. The VMs follows the hostname convention: `bds-g<group_id>-n<{0,1,2}>`.

The assigned VMs can be found at the [virtualresources](https://virtualresources.sdu.dk) portal from the local SDU network. Use VPN when home!

The VMs assosiated to your SDU profile will appear on the portal. 
Watch the video [here](https://www.youtube.com/watch?v=iKM6P7nRzqI&feature=youtu.be) to learn how to navigate the portal and to learn how to get your SSH keys for your VMs.

## Links
- [SDU VPN](https://any.sdu.dk)
- [virtualresources.sdu.dk](https://virtualresources.sdu.dk)
- [Kubernetes command-line tool - kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
- [microk8s.io](https://microk8s.io)
- [kubernetes.io](https://kubernetes.io)

## VM Sepcifications
- Ubuntu 20.04.6 LTS
- 50GB disk
- 8GB RAM
- 2 CPU cores

## Adding new user to the VM


For late-coming students or student who changes group during the semester and need to get access to the VMs. do the following:

1. Talk and confirm your situation with the project supervisor.
1. Reach out to the instructors at this course who can update the group members in [virtualresources.sdu.dk](https://virtualresources.sdu.dk). 
1. The next step is to add your SDU username to each of the associated VMs in the group. The procedure to follow is listed below and must be replicated multiple times on each of the VMs. For the following steps, you need assistance from a group member who already has access to the VMs.
With help from your group member follow the next steps:
    1. Add a new user to the VM: `sudo useradd <SDU username> -m`. 
    1. Add created user to the group: `sudo usermod <SDU username> -G <SDU username>`.
    1. Create a `.ssh` folder in the home directory: `sudo mkdir -p /home/<SDU username>/.ssh/` 
    1. Create a `authorized_keys` file: 
        1. Enter root user: `sudo su`
        1. `sudo echo "" > /home/<SDU username>/.ssh/authorized_keys`
        1. Copy and paste the content of the public key (`id_rsa_scalable_<SDU username>.pub`) from [virtualresources.sdu.dk](https://virtualresources.sdu.dk) into the `/home/<SDU username>/.ssh/authorized_keys` file. 
        1. exit root user: `exit`
1. SSH into the VMs from your localhost.


## SSH
Will will be able to login to the VMs using a SSH connection. You need to download the config file and SSH keys from [virtualresources.sdu.dk](https://virtualresources.sdu.dk) before being able to login. 

**NB:** You need to update the permissions on the downloaded config file and SSH keys.

### UNIX - Updating the permission

Run the following code chunk to set the proper owner and rigths of the config file and the SSH keys.

```zsh
chown -R $USER:$USER ~/.ssh
chmod -R 700 ~/.ssh
```

## MicroK8s
The VM ships with [microk8s.io](https://microk8s.io) and the VMs have been initilized to form a Kubernetes cluster with three nodes.

The following installition process have been performed on each individual VM.

### Installation and setting up the Kubernetes on each VM
1. Install MicroK8s on Ubuntu
    ```zsh
    sudo apt update
    sudo apt install -y snapd
    sudo snap install microk8s --classic
    ```

1. Add `$USER` to `microk8s` group
    ```zsh
    sudo usermod -a -G microk8s $USER
    mkdir ~/.kube
    sudo chown -R $USER ~/.kube
    newgrp microk8s
    ```

1. Check the status while Kubernetes initializing
    ```zsh
    microk8s status --wait-ready
    ```

1. Enable the services you need
    ```zsh
    microk8s enable hostpath-storage
    ```

### Setting up the Kubernetes cluster
The following steps demostrates how to bind the three VMs into one cluster.

1. Open three terminal windows and SSH into each of your machines.
    ```zsh
    ssh bds-g<group_id>-n<{0,1,2}>
    ```

1. Use the `microk8s add-node` command on node `bds-g<group_id>-n0` twice. Each command is producing a command you need to copy and paste into your other terminal windows (your active SSH session with `bds-g<group_id>-n1` and `bds-g<group_id>-n2`).
    ```zsh
    anbae@bds-g<group_id>-n0:~$ microk8s add-node 
        From the node you wish to join to this cluster, run the following:
        microk8s join <IP>:25000/<TOKEN>

        Use the '--worker' flag to join a node as a worker not running the control plane, eg:
        microk8s join <IP>:25000/<TOKEN> --worker

        If the node you are adding is not reachable through the default interface you can use one of the following:
        microk8s join <IP>:25000/<TOKEN>
    ```
1. `microk8s join <IP>:25000/<TOKEN>`
1. `microk8s join <IP>:25000/<TOKEN>`
1. Get status on your Kubernetes cluster
    ```zsh
    anbae@bds-g<group_id>-n0:~$ microk8s status 
        microk8s is running
        high-availability: yes
            datastore master nodes: <IP bds-g<group_id>-n0>:19001 <IP bds-g<group_id>-n1>:19001 <IP bds-g<group_id>-n2>:19001
        ...
        ...
        ...
    ```
1. List nodes in your Kubernetes cluster
    ```zsh
    anbae@bds-g<group_id>-n0:~$ microk8s kubectl get nodes 
        NAME                    STATUS   ROLES    AGE   VERSION
        bds-g<group_id>-n1      Ready    <none>   61m   v1.27.5
        bds-g<group_id>-n2      Ready    <none>   60m   v1.27.5
        bds-g<group_id>-n0      Ready    <none>   18h   v1.27.5
    ```

## Connect to your Kubernetes cluster

> We recommend to run `kubectl` commands from your localhost. 

In order to follow our recommendations, you need to update your kubeconfig file on your localhost and remember to keep an open a SSH session to one of your VMs during exercise hours and project work. The local updates are explained in the following sections.

### kubeconfig

By default, `kubectl` looks for a file called `config` inside the the `.kube` folder in your home directory. To use a different kubeconfig file you can use `kubectl --kubeconfig <path to config>`.

A kubeconfig file may look like this:

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://127.0.0.1:16443
  name: microk8s-cluster
contexts:
- context:
    cluster: microk8s-cluster
    user: admin
  name: microk8s
current-context: microk8s
kind: Config
preferences: {}
users:
- name: admin
  user:
    token: REDACTED
```

The config contains three lists: `clusters`, `users` and `contexts`:

- `clusters` is a list of Kubernetes clusters. It has the URI to the Kubernetes API and a certificate for the Kubernetes certificate authority.
- `users` is a list of users. It contains information used to authenticate the user.
- `contexts` is a list of contexts. A context associates a cluster and a user.

The name property for clusters, users and contexts can be anything. It is just a key to identify the cluster, context or user in the config file.

The `current-context` property is used to tell `kubectl` what context to use. It can be changed manually by modifying the file, or using kubectl: `kubectl config use-context <context name>`.

For further information, please look into [Organizing Cluster Access Using kubeconfig Files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) if you need to manage multiple Kubernetes environments.

### Retrieving kubeconfig from the VM

A single MicroK8s cluster has been set up on the VMs. 
The kubeconfig for MicroK8s is located at `/var/snap/microk8s/current/credentials/client.config`. Open a SSH session to any of the VMs and copy the file to your localhost. Then proceed to next section.

### Interacting with the Kubernetes cluster from your localhost

You can either merge the `config` file from MicroK8s into your existing kubeconfig file, which is recommended, or you can specify a non-default `config` using the `--kubeconfig` argument in `kubectl`.

If you merge the `config` file, then simply copy the entries from the `clusters`, `users` and `contexts` lists to your exsisting kubeconfig file inside the `.kube` folder in your home directory.

**Note:** Please note that you need to use `127.0.0.1`.
