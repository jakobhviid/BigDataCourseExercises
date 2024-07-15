#!/bin/bash


echo "Creating namespaces in kubernetes!"
while read p; do
  kubectl create ns $p
done <users.txt