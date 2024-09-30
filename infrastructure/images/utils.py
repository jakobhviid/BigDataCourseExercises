import os
from pathlib import Path

TARGET_REGISTRY: str = "registry.gitlab.sdu.dk/jah/bigdatarepo"
FILENAME: Path = Path(__file__).absolute().parent / "images.txt"
MAPPING = {
    "paulbouwer/hello-kubernetes:1.10.1": {
        "image_name": "hello-kubernetes",
        "image_tag": "1.10.1",
    },
    "ubuntu:24.04": {"image_name": "ubuntu", "image_tag": "24.04"},
    "bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8": {
        "image_name": "hadoop-namenode",
        "image_tag": "2.0.0-hadoop3.2.1-java8",
    },
    "bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8": {
        "image_name": "hadoop-datanode",
        "image_tag": "2.0.0-hadoop3.2.1-java8",
    },
    "apache/hadoop:3": {"image_name": "hadoop", "image_tag": "3"},
    "bitnami/kafka:3.8.0-debian-12-r3": {
        "image_name": "kafka",
        "image_tag": "3.8.0-debian-12-r3",
    },
    "confluentinc/cp-schema-registry:7.3.1": {
        "image_name": "cp-schema-registry",
        "image_tag": "7.3.1",
    },
    "confluentinc/cp-ksqldb-server:7.3.1": {
        "image_name": "cp-ksqldb-server",
        "image_tag": "7.3.1",
    },
    "confluentinc/cp-ksqldb-cli:7.3.1": {
        "image_name": "cp-ksqldb-cli",
        "image_tag": "7.3.1",
    },
    "redpandadata/console:v2.7.1": {
        "image_name": "redpanda-console",
        "image_tag": "v2.7.1",
    },
    "bitnami/postgresql:15.1.0-debian-11-r12": {
        "image_name": "postgresql",
        "image_tag": "15.1.0-debian-11-r12",
    },
    "dvoros/sqoop:latest": {"image_name": "sqoop", "image_tag": "latest"},
    "bde2020/flume:latest": {"image_name": "flume", "image_tag": "latest"},
    "bitnami/spark:3.5.2-debian-12-r1": {
        "image_name": "spark",
        "image_tag": "3.5.2-debian-12-r1",
    },
    "rtdl/hive-metastore:3.1.2": {"image_name": "hive-metastore", "image_tag": "3.1.2"},
    "apache/hive:3.1.3": {"image_name": "hive", "image_tag": "3.1.2"},
    "mongo:latest": {"image_name": "mongo", "image_tag": "latest"},
    "mongo-express:latest": {"image_name": "mongo-express", "image_tag": "latest"},
    "bitnami/redis-cluster:7.4.0-debian-12-r1": {
        "image_name": "redis-cluster",
        "image_tag": "7.4.0-debian-12-r1",
    },
}


def read_images_file(file_name: Path) -> list[str]:
    with open(file_name, "r") as f:
        images = f.read().splitlines()
    return images


def get_new_image_name(image_name: str, image_tag: str) -> str:
    return f"{TARGET_REGISTRY}/{image_name}:{image_tag}"


def pull_tag_push(image_name: str, new_image_name: str) -> None:
    os.system(f"docker pull {image_name}")
    os.system(f"docker tag {image_name} {new_image_name}")
    os.system(f"docker push {new_image_name}")


def pull_save_import(image_name: str) -> None:
    os.system(f"docker pull {image_name}")
    os.system(f"docker save {image_name} > image.tar")
    os.system("microk8s images import < image.tar")
    os.system("rm image.tar")
