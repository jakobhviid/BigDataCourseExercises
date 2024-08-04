#!/bin/bash

echo "Create kubeconfigs!"
while read p; do
  NAMESPACE=$p ./create-user.sh 
done <users.txt