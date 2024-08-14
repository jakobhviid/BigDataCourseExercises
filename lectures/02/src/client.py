from hdfs import InsecureClient

HDFS_HOSTS: list[str] = ["http://namenode:9870"]
HDFS_USER_NAME: str = "root"


def get_hdfs_client() -> InsecureClient:
    return InsecureClient(";".join(HDFS_HOSTS), user=HDFS_USER_NAME)
