#!/bin/sh
tag=latest
containername=anbae-big-data-course
dockerhubacc=anderslaunerbaek
imagename=$dockerhubacc/$containername:$tag

echo $imagename
docker build --tag=$imagename .
# # docker run -it $imagename
# # docker login
docker push $imagename
