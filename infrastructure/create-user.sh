#!/bin/bash

# Accept server and namespace as arguments
SERVER=$1
NAMESPACE=$2

# Variables
SERVICE_ACCOUNT="${NAMESPACE}-sa"
ROLE="${NAMESPACE}-role"
ROLE_BINDING="${NAMESPACE}-rolebinding"
CLUSTER_ROLE="view-clusterrole"
CLUSTER_ROLE_BINDING="${NAMESPACE}-view-clusterrolebinding"
SECRET_NAME="${SERVICE_ACCOUNT}-manual-secret"
CA_CERT="/var/snap/microk8s/current/certs/ca.crt"
KUBECONFIG_DIR="tmp"

# Create namespace if it doesn't exist
microk8s kubectl get namespace $NAMESPACE || microk8s kubectl create namespace $NAMESPACE || { echo "Failed to create namespace. Exiting."; exit 1; }

# Create ServiceAccount if it doesn't exist
microk8s kubectl get serviceaccount $SERVICE_ACCOUNT -n $NAMESPACE || microk8s kubectl create serviceaccount $SERVICE_ACCOUNT -n $NAMESPACE || { echo "Failed to create ServiceAccount. Exiting."; exit 1; }


# Create Role for full CRUD permissions denoted by (*) within the specific namespace
cat <<EOF | microk8s kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: $NAMESPACE
  name: $ROLE
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["get", "list", "watch", "create", "update", "delete", "patch"]
EOF

# Create RoleBinding for full CRUD permissions within the specific namespace
cat <<EOF | microk8s kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: $ROLE_BINDING
  namespace: $NAMESPACE
subjects:
- kind: ServiceAccount
  name: $SERVICE_ACCOUNT
  namespace: $NAMESPACE
roleRef:
  kind: Role
  name: $ROLE
  apiGroup: rbac.authorization.k8s.io
EOF


# Create ClusterRole for read-only permissions across all namespaces denoted by (*)
cat <<EOF | microk8s kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: $CLUSTER_ROLE
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
EOF

# Create ClusterRoleBinding for read-only permissions across all namespaces
cat <<EOF | microk8s kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: $CLUSTER_ROLE_BINDING
subjects:
- kind: ServiceAccount
  name: $SERVICE_ACCOUNT
  namespace: $NAMESPACE
roleRef:
  kind: ClusterRole
  name: $CLUSTER_ROLE
  apiGroup: rbac.authorization.k8s.io
EOF

# Manually create the secret with proper annotations
cat <<EOF | microk8s kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: $SECRET_NAME
  namespace: $NAMESPACE
  annotations:
    kubernetes.io/service-account.name: $SERVICE_ACCOUNT
type: kubernetes.io/service-account-token
EOF

# Wait for the secret to be populated
sleep 10

# Extract the token from the secret
TOKEN=$(microk8s kubectl get secret $SECRET_NAME -n $NAMESPACE -o jsonpath="{.data.token}" | base64 --decode) || { echo "Failed to retrieve token. Exiting."; exit 1; }

# Ensure TOKEN is available
if [ -z "$TOKEN" ]; then
  echo "Error: Token not found or created for ServiceAccount $SERVICE_ACCOUNT in namespace $NAMESPACE"
  exit 1
else
  echo "Token for ServiceAccount $SERVICE_ACCOUNT in namespace $NAMESPACE: $TOKEN"
fi

# Extract the certificate authority data
CERTIFICATE_AUTHORITY_DATA=$(cat $CA_CERT | base64 | tr -d '\n') || { echo "Failed to read CA certificate. Exiting."; exit 1; }

# Create kubeconfig directory if not exists
mkdir -p $KUBECONFIG_DIR

# Create kubeconfig file
cat <<EOF > $KUBECONFIG_DIR/$NAMESPACE-kubeconfig.yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: ${CERTIFICATE_AUTHORITY_DATA}
    server: ${SERVER}
  name: microk8s-cluster
contexts:
- context:
    cluster: microk8s-cluster
    namespace: $NAMESPACE
    user: $NAMESPACE
  name: $NAMESPACE-context
current-context: $NAMESPACE-context
users:
- name: $NAMESPACE
  user:
    token: ${TOKEN}
EOF

echo "Kubeconfig file for $NAMESPACE created successfully at $KUBECONFIG_DIR/$NAMESPACE-kubeconfig.yaml"
