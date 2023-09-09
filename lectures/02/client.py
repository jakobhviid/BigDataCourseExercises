from hdfs import InsecureClient 


HDFS_URL: str = "http://simple-hdfs-namenode-default-0"
HDFS_PORT: str = "9870"
HDFS_USERNAME: str = "stackable"


def get_hdfs_client() -> InsecureClient:
    return InsecureClient(f"{HDFS_URL}:{HDFS_PORT}", user=HDFS_USERNAME)