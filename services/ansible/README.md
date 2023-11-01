# 3. semester project Kubernetes

## Prerequisites

Fill out values:

* ./inventory/cluster/hosts.yml - the hostnames / ips of the servers.
* ./vars/teams.yml - the name of the teams will be whatever you write in the teams list
* ./kubeconfig.yml - replace it with the admin kubeconfig
* ./playbooks/cluster-installation.yml - replace with appropriate values
* ./playbooks/cluster-namespaces.yml - replace "base64 of gitlab token"
* ./templates/kubeconfig.j2 - replace values. "certificate-authority-data" and "server" should just be the same as the one from the admin kubeconfig

## Operations

**Install cluster**

`ansible-playbook -i ./inventory/hosts.yml cluster-installation.yml`

Admin kubeconfig is located at `/etc/rancher/k3s/k3s.yaml` on a controlplane node.

**Uninstall cluster**

`ansible-playbook -i ./inventory/hosts.yml cluster-installation.yml --become -e 'k3s_state=uninstalled'`

**Create kubeconfig for each team**

`ansible-playbook cluster-teams.yml`

**Create and prepare namespaces**

`ansible-playbook cluster-namespaces.yml`
