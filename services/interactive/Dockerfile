ARG UBUNTU_VERSION=22.04

FROM ubuntu:${UBUNTU_VERSION}

RUN apt-get update && apt install software-properties-common -yq tzdata \
    && ln -fs /usr/share/zoneinfo/Europa/Copenhagen /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update \
    && apt install -y python3.11 python3-pip \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 \
    && rm -rf /var/lib/apt/lists/*

USER root
WORKDIR /home/root