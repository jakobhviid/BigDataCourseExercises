#!/bin/bash

# Check if the server IP argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <server-ip>"
  exit 1
fi

SERVER_IP=$1
SERVER="https://${SERVER_IP}:16443"

# Check if MicroK8s is running
microk8s status --wait-ready || { echo "MicroK8s is not running. Exiting."; exit 1; }

# Paths to certificates
CA_CERT="/var/snap/microk8s/current/certs/ca.crt"
CLIENT_CERT="/var/snap/microk8s/current/certs/client.crt"
CLIENT_KEY="/var/snap/microk8s/current/certs/client.key"

# Extract certificates as base64
CERTIFICATE_AUTHORITY_DATA=$(cat $CA_CERT | base64 | tr -d '\n') || { echo "Failed to read CA certificate. Exiting."; exit 1; }
CLIENT_CERTIFICATE_DATA=$(cat $CLIENT_CERT | base64 | tr -d '\n') || { echo "Failed to read client certificate. Exiting."; exit 1; }
CLIENT_KEY_DATA=$(cat $CLIENT_KEY | base64 | tr -d '\n') || { echo "Failed to read client key. Exiting."; exit 1; }

# Create kubeconfig file
cat <<EOF > admin-kubeconfig.yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: ${CERTIFICATE_AUTHORITY_DATA}
    server: ${SERVER}
  name: bds-cluster
contexts:
- context:
    cluster: bds-cluster
    user: bds-admin
  name: bds-microk8s
current-context: bds-microk8s
kind: Config
preferences: {}
users:
- name: bds-admin
  user:
    client-certificate-data: ${CLIENT_CERTIFICATE_DATA}
    client-key-data: ${CLIENT_KEY_DATA}
EOF

echo "Admin kubeconfig created successfully at admin-kubeconfig.yaml"