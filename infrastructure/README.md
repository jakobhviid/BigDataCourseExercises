# Setup infrastructure to instructors
The main idea is that the students only have to install the `kubectl` client. The instructors will setup the infrastructure and the students will only have to connect to the Kubernetes cluster though `<IP>:16443`.

## Install Kubernetes distribution
We have chosen to use the [Microk8s](https://microk8s.io) distribution for this course. It is a lightweight distribution that is easy to install and manage. The distribution runs on bare metal and not containerized simulators like Minikube.

```bash
sudo snap install microk8s --classic
microk8s status --wait-ready
```

### Addons
We will enable the following addons:

```bash
microk8s enable cert-manager
microk8s enable rbac
microk8s enable dns
```


## Create workspace and service accounts for students
We will create a namespace, a service account, and a role for each namespace. The service account will be used together with a role binding to create a kubeconfig file for each of the students.

The above-mentioned steps are automated in the script [create-user.sh](create-user.sh). The file [create-users.sh](create-users.sh) parses the file [users.txt](users.txt) which includes a list of students for which we want to create access for.


### Step by step
1. Ensure the students are listed in the file `users.txt`
2. Run the following command to create the users on a Kubernetes node running the Microk8s distribution:
```bash
./create-users.sh "<IP>"
```
3. The script outputs the kubeconfig files for each student in the folder `~/tmp/<namespace>-kubeconfig.yaml`
4. Distribute the kubeconfig files to the students.


## Course project

WIP - Todo
- Create namespace for each project
- Map proper service accounts to each project