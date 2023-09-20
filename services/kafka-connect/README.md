# Kafka Connect

This folder includes the build recipe and components for the used image running with the following pre-built connectors:
- [mongodb/kafka-connect-mongodb:1.8.0](https://www.confluent.io/hub/mongodb/kafka-connect-mongodb)
- [confluentinc/kafka-connect-jdbc:latest](https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc)
- [confluentinc/kafka-connect-hdfs:latest](https://docs.confluent.io/kafka-connectors/hdfs/current/overview.html)

This image is based on `confluentinc/cp-server-connect-base:7.3.1` and the above-mentioned connectors have been added to extend the base image. Please look into the [Dockerfile](./Dockerfile) for greater context.

The new image has been built and published to Docker Hub: [`anderslaunerbaek/cp-server-connect-base:lec03hdfs2`](https://hub.docker.com/layers/anderslaunerbaek/cp-server-connect-base/lec03hdfs2/images/sha256-14061e5836a45b391d723d50231d08f2808cd7839dc168eadea01c9e880e0e1f?context=repo) for ease of use later in Kubernetes.

## Next step
Look into the [kafka-extra.yaml](./../../lectures/03/kafka-extra.yaml) file and find the Kubernetes deployment called `kafka-connect` and see how this service integrates with the other transport and streaming services.