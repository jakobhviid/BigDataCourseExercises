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

## Add custom domain to Kubernetes API Certificates

1. Update the csr.conf.template in ´certs´ folder in the ´microk8s´ cluster

````bash
sudo nano /var/snap/microk8s/current/certs/csr.conf.template
````

2. Add the new custom domain 

````
...

[ alt_names ]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster
DNS.5 = kubernetes.default.svc.cluster.local
DNS.6 = CUSTOM-DOMAIN (Added)
IP.1 = 127.0.0.1
IP.2 = xxx.xxx.xxx.xxx
IP.3 = SERVER_IP (Added, only if errors)
#MOREIPS

...
````

3. Sign the CSR with the existing CA to generate a new server certificate

````bash
sudo openssl x509 -req -in /var/snap/microk8s/current/certs/server.csr -CA /var/snap/microk8s/current/certs/ca.crt -CAkey /var/snap/microk8s/current/certs/ca.key -CAcreateserial -out /var/snap/microk8s/current/certs/server.crt -days 365 -extensions v3_ext -extfile /var/snap/microk8s/current/certs/csr.conf.template
````

4. Restart MicroK8s Services

````bash
sudo microk8s stop
sudo microk8s start
````

## Side-load container images
We will side-load the container images onto cluster in advanced in order to improve latency and limit network load. The current approach is described here. Execute the [side-load.sh](./side-load.sh) file to load the images presented in the [images.txt](./images.txt) file into the cluster.

## Observability
The Microk8s addon `observability` provides information about the Kubernetes cluster utilizing Prometheus to scape the K8's cluster.
To gain an overview of the cluster health and load, the addon comes with Grafana. The steps below shows how to gain access to the Grafana Dashboards.


1. Get the Grafana Stack credentials

````bash
microk8s kubectl get secret -n observability kube-prom-stack-grafana -o jsonpath="{.data.admin-user}" | base64 --decode; echo
microk8s kubectl get secret -n observability kube-prom-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode; echo
````

2. Identify the Grafana Stack pod

````bash
kubectl get pods -n observability
````

3. Port-forward the Grafana Stack pod

````bash
kubectl port-forward -n observability kube-prom-stack-grafana-8dc65649-82k98 3000:3000
````

4. Enter the credentials

## Course project

WIP - Todo
- Create namespace for each project
- Map proper service accounts to each project