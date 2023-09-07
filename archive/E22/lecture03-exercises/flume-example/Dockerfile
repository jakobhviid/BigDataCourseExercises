# Using standard ubuntu LTS version
FROM ubuntu:18.04
# Settings labels
# Originally: LABEL Name=flume Version=0.0.1 Maintainer="Jakob Hviid <jah@mmmi.sdu.dk>"
# Changed by Group 05, SDU 2021

# installing needed packages
RUN apt-get update 
RUN apt-get install -y wget openjdk-8-jre-headless vim nano telnet
RUN apt-get autoremove -y
RUN apt-get clean

# Getting FLume Binaries and readying the folder in /flume
RUN wget https://archive.apache.org/dist/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz
RUN tar -zxvf apache-flume-1.9.0-bin.tar.gz
RUN rm apache-flume-1.9.0-bin.tar.gz
RUN mv apache-flume-1.9.0-bin flume

# Setting up environment variables
RUN echo 'export FLUME_HOME=/flume/' >> ~/.bashrc
RUN echo 'export PATH=$PATH:$FLUME_HOME/bin/' >> ~/.bashrc
RUN echo 'export PATH=$PATH:$FLUME_HOME/bin/flume-ng' >> ~/.bashrc
# RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/jre/' >> ~/.bashrc # CHANGE DEPENDING ON CHIP ARCHITECTURE
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-arm64/jre/' >> ~/.bashrc
# RUN export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/jre/ # CHANGE DEPENDING ON CHIP ARCHITECTURE
RUN export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-arm64/jre/

ENV FLUME_HOME=/flume/
ENV PATH=$PATH:$FLUME_HOME/bin/
ENV PATH=$PATH:$FLUME_HOME/bin/flume-ng
# ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/jre/ # CHANGE DEPENDING ON CHIP ARCHITECTURE
ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-arm64/jre/

# Readying for example code
EXPOSE 44444

WORKDIR /flume

ADD flume.conf /flume/conf/
# /bin/bash required to recognize the environment variables
ENTRYPOINT [ "/bin/bash", "-c", "flume-ng agent --conf ./conf/ -f ./conf/flume.conf --name KafkaAgent -Dflume.root.logger=INFO,console" ] 