# Setup infrastructure to instructors

The main idea is that the students only have to install the `kubectl` client. The instructors will setup the infrastructure and the students will only have to connect to the Kubernetes cluster though `<IP>:16443`.

## Install Kubernetes distribution

We have chosen to use the [Microk8s](https://microk8s.io) distribution for this course. It is a lightweight distribution that is easy to install and manage. The distribution runs on bare metal and not containerized simulators like Minikube.

```bash
sudo snap install microk8s --classic
microk8s status --wait-ready
```

### Addons

Addons enabled by default

````bash
ha-cluster
helm
helm3
````

We will enable the following addons:

```bash
microk8s enable cert-manager
microk8s enable rbac
microk8s enable dns
microk8s enable observability (Will also enable hostpath-storage and storage)
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
4. Distribute the kubeconfig files to the students using SDU email. Inspiration is found here: [sent_msg_students.py](./share_kubeconfigs/sent_msg_students.py).

### Course project

The setup of the projects will be utilizing same namespace and service account approach as mentioned above. Therefore, update the content of the [users.txt](users.txt) file and follow the three first steps as above. Use the following file [sent_msg_groups.py](./share_kubeconfigs/sent_msg_groups.py) to distribute the kubeconfig to each group member.

## Share the kubeconfig file with the students

The kubeconfig file is the configuration file that the students will use to connect to the Kubernetes cluster. The file is generated in the previous step and should be shared with the students in a secure manner.

The current approach is to share the file through a secure messaging service directly to the students SDU email account. Please use a similar examples as this Python [sent_msg.py](./share_kubeconfigs/sent_msg.py) script to share the kubeconfig files.

## Add custom domain to Kubernetes API Certificates

1. Update the csr.conf.template in ´certs´ folder in the ´microk8s´ cluster

    ````bash
    sudo nano /var/snap/microk8s/current/certs/csr.conf.template
    ````

2. Add the new custom domain

    ````text
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

We will side-load the container images onto cluster in advanced in order to improve latency and limit network load. The current approach is described here. Execute the [side-load.sh](./images/side-load.sh) file or the [side-load.py](./images/side-load.py) file to load the images presented in the [images.txt](./images/images.txt) file into the cluster.

## Persist images

We will off-load the container images onto [gitlab.sdu.dk](https://gitlab.sdu.dk/jah/bigdatarepo/container_registry) to ensure reproducibility. Execute the [persist-images.py](./images/persist-images.py) file to pull, re-tag, and push the used images presented in the [images.txt](./images/images.txt) file.

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

## Adjusting max pod limit

By default, a single node can only contain `110` pods. To increase the pod limit, follow the steps below:

1. Open the MicroK8s kubelet configuration file

    ````bash
    sudo nano /var/snap/microk8s/current/args/kubelet
    ````

2. Modify or add the `max-pods` setting to the desired amount e.g 1500

    ````bash
    --max-pods=1500
    ````

3. Save and close the file

4. Restart the microK8s cluster

    ````bash
    sudo microk8s.stop
    sudo microk8s.start
    ````

5. Verify the change

    ````bash
    kubectl describe node <your-node-name> 
    ````
