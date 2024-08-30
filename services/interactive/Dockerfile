ARG UBUNTU_VERSION=22.04

FROM ubuntu:${UBUNTU_VERSION}


COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
ENV JAVA_HOME=/usr/local/openjdk-8
RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

RUN apt-get update && apt install software-properties-common -yq tzdata \
    && ln -fs /usr/share/zoneinfo/Europa/Copenhagen /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update \
    && apt install -y python3.12 \
    && apt install -y curl \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1
# #\
# #     # && update-alternatives --config python \
# #     && rm -rf /var/lib/apt/lists/*


#     # Restart your shell for the changes to take effect.

#     # Load pyenv-virtualenv automatically by adding
#     # the following to ~/.bashrc:
ENV PYSPARK_PYTHON=python
ENV PYSPARK_DRIVER_PYTHON=python
USER root
WORKDIR /home/root/code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


# # ENTRYPOINT [ "bash" ]
# # CMD ["/bin/sleep", "3650d"]
# # CMD ["bash"]
# # CMD ["#!/bin/bash"]
# # CMD ["/bin/ping", "localhost"]


# FROM python:3.12

# COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
# ENV JAVA_HOME=/usr/local/openjdk-8
# RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

# # ARG UBUNTU_VERSION=22.04

# # FROM ubuntu:${UBUNTU_VERSION}

# # ENV LANG=en_US.UTF-8
# # ENV LANGUAGE=en_US.UTF-8

# # RUN apt-get update && apt install software-properties-common -yq tzdata \
# #     && ln -fs /usr/share/zoneinfo/Europa/Copenhagen /etc/localtime \
# #     && dpkg-reconfigure -f noninteractive tzdata \
# #     && add-apt-repository ppa:deadsnakes/ppa \
# #     && apt update \
# #     && apt-get install -qq openjdk-8-jdk-headless  \
# #     && apt install -y python3.12 python3-pip \
# #     && apt install -y curl \
# #     && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

# # RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1
# # #\
# # #     # && update-alternatives --config python \
# # #     && rm -rf /var/lib/apt/lists/*


# #     # Restart your shell for the changes to take effect.

# #     # Load pyenv-virtualenv automatically by adding
# #     # the following to ~/.bashrc:
# USER root
# WORKDIR /home/root/code
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

# ENV PYSPARK_PYTHON=python
# ENV PYSPARK_DRIVER_PYTHON=python

# # ENTRYPOINT [ "bash" ]
# # CMD ["sleep", "infinity"]
# # CMD ["bash"]
# # CMD ["#!/bin/bash"]
# # CMD ["/bin/ping", "localhost"]
# ENTRYPOINT ["/bin/sh", "-c" , "echo Hello World", "tail -f /dev/null"]
