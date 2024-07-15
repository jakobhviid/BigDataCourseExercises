#!/bin/bash
# https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/#normal-user

mkdir -p tmp
echo "Creating certificates for kubernetes!"
while read p; do
  # kubectl create ns $p
  echo "$p"


  # step 1.1: generate private key
  openssl genrsa -out tmp/$p.key 2048

  # step 1.2: generate csr
  openssl req -new -key tmp/$p.key -out tmp/$p.csr -subj "/CN=$p"

  # step 1.3: base64 encode the csr
  export CSR_BASE64="$(cat tmp/$p.csr | base64 | tr -d "\n")"

  # step 1.4: create a certificate signing request
  export USER="$p"
  # envsubst < user_cert.yaml | kubectl apply -f -
  echo "$(envsubst < user_cert.yaml)" > tmp/$p.yaml
  kubectl apply -f tmp/$p.yaml

  # step 1.5: approve the certificate signing request
  # kubectl get csr
  kubectl certificate approve $p

  # step 1.6: get the certificate
  kubectl get csr $p -o jsonpath='{.status.certificate}'| base64 -d > tmp/$p.crt


  # step 2.1: create role and rolebinding
  #kubectl create role developer-$p --namespace=$p --verb=create --verb=get --verb=list --verb=update --verb=delete --resource=pods
  #kubectl create rolebinding developer-binding-$p --namespace=$p --role=developer-$p --user=$p
done <users.txt


# kubectl config set-credentials user01 --client-key=tmp/user01.key --client-certificate=tmp/user01.crt --embed-certs=true
# kubectl config set-context user01 --cluster=microk8s-cluster --user=user01 --namespace=user01