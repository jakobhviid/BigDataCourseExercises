docker build . -t pymaria:latest 
docker run --rm --network datahub_network --name pymaria pymaria