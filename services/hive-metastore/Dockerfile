# Use an official openjdk runtime as a parent image
FROM openjdk:8-jdk

# Set environment variables
ENV HIVE_VERSION=3.1.2
ENV JAVA_HOME=/usr/local/openjdk-8
ENV HIVE_HOME=/opt/hive-${HIVE_VERSION}

# Install dependencies
RUN apt-get update && apt-get install -y wget tar procps

# Download and install Hive from Apache Archive
RUN wget https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz && \
    tar -xzvf apache-hive-${HIVE_VERSION}-bin.tar.gz -C /opt && \
    mv /opt/apache-hive-${HIVE_VERSION}-bin /opt/hive-${HIVE_VERSION} && \
    rm apache-hive-${HIVE_VERSION}-bin.tar.gz

# Set up Hive environment variables
ENV PATH=$PATH:${HIVE_HOME}/bin

# Expose the Thrift port
EXPOSE 9083

# Entry point for starting the Hive Metastore
ENTRYPOINT ["hive", "metastore"]
CMD ["-p", "9083"]
