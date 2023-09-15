#!/bin/sh
tag=7.3.1
containername=cp-server-connect-base
dockerhubacc=anderslaunerbaek
imagename=$dockerhubacc/$containername:$tag

echo $imagename
docker build --build-arg="CP_VERSION=$tag" --tag=$imagename  . 
# # docker run -it $imagename
# # docker login
docker push $imagename
