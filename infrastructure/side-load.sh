#!/bin/bash

echo "Image side loading!"
while read IMAGE; do
  echo docker image: $IMAGE
  sudo docker pull $IMAGE
  sudo docker save $IMAGE > image.tar
  microk8s images import < image.tar
done <images.txt
rm image.tar