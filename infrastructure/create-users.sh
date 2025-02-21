#!/bin/bash

# Check if the server IP argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <server-ip>"
  exit 1
fi

SERVER_IP=$1
# SERVER_IP="bd.hviid.phd"
# SERVER_IP="10.123.3.156"
SERVER="https://${SERVER_IP}:16443"

# # Check if MicroK8s is running
# microk8s status --wait-ready || { echo "MicroK8s is not running. Exiting."; exit 1; }

# # Enable necessary addons
# microk8s enable rbac dns cert-manager || { echo "Failed to enable addons. Exiting."; exit 1; }

echo "Create kubeconfigs!"
# while read NAMESPACE,SERVICE_ACCOUNT; do

while IFS=',' read -r SERVICE_ACCOUNT NAMESPACE
do 
  ./create-user.sh "$SERVER" "$NAMESPACE" "$SERVICE_ACCOUNT"
done <users.txt