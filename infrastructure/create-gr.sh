#!/bin/bash

# Accept group name and username as arguments
NAMESPACE_GROUP=$1
NAMESPACE_USER=$2

# Variables
SERVICE_ACCOUNT="${NAMESPACE_USER}-sa"
ROLE="${NAMESPACE_GROUP}-${NAMESPACE_USER}-role"
ROLE_BINDING="${NAMESPACE_GROUP}-${NAMESPACE_USER}-rolebinding"

# Create namespace if it doesn't exist
kubectl get namespace $NAMESPACE_GROUP || kubectl create namespace $NAMESPACE_GROUP || { echo "Failed to create namespace. Exiting."; exit 1; }

# Create Role for full CRUD permissions denoted by (*) within the specific namespace
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: $NAMESPACE_GROUP
  name: $ROLE
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["get", "list", "watch", "create", "update", "delete", "patch"]
EOF

# Create RoleBinding for full CRUD permissions within the specific namespace
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: $ROLE_BINDING
  namespace: $NAMESPACE_GROUP
subjects:
- kind: ServiceAccount
  name: $SERVICE_ACCOUNT
  namespace: $NAMESPACE_GROUP
roleRef:
  kind: Role
  name: $ROLE
  apiGroup: rbac.authorization.k8s.io
EOF

