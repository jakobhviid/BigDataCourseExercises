from hdfs import InsecureClient

HDFS_HOSTS: list[str] = [
    "http://simple-hdfs-namenode-default-0.simple-hdfs-namenode-default:9870",
    "http://simple-hdfs-namenode-default-1.simple-hdfs-namenode-default:9870",
]
HDFS_USER_NAME: str = "stackable"


def get_hdfs_client() -> InsecureClient:
    return InsecureClient(";".join(HDFS_HOSTS), user=HDFS_USER_NAME)
