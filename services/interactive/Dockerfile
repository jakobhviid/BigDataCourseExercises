ARG UBUNTU_VERSION=22.04

FROM ubuntu:${UBUNTU_VERSION}

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
ENV JAVA_HOME=/usr/local/openjdk-8
RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

RUN apt-get update && apt install software-properties-common -yq tzdata \
    && ln -fs /usr/share/zoneinfo/Europa/Copenhagen /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update \
    && apt install -y python3.12 \
    && apt install -y curl \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 \
    # Install HDFS CLI
    && curl -O https://archive.apache.org/dist/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz \
    && tar xzf hadoop-3.2.1.tar.gz \
    && rm hadoop-3.2.1.tar.gz \
    && mv hadoop-3.2.1 /usr/local/hadoop

ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin
ENV PATH=$PATH:$HADOOP_HOME/sbin
ENV HADOOP_MAPRED_HOME=$HADOOP_HOME
ENV HADOOP_COMMON_HOME=$HADOOP_HOME
ENV HADOOP_HDFS_HOME=$HADOOP_HOME
ENV YARN_HOME=$HADOOP_HOME
ENV HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
ENV HADOOP_OPTS=-Djava.library.path=$HADOOP_HOME/lib

ENV PYSPARK_PYTHON=python
ENV PYSPARK_DRIVER_PYTHON=python
USER root
WORKDIR /home/root/code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt