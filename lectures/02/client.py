from hdfs import InsecureClient

HDFS_HOSTS = [
    "http://simple-hdfs-namenode-default-0.simple-hdfs-namenode-default:9870",
    "http://simple-hdfs-namenode-default-1.simple-hdfs-namenode-default:9870"
]
HDFS_USER_NAME: str = "stackable"

def get_hdfs_client() -> InsecureClient:
    url = ""
    for host in HDFS_HOSTS:
        url += host + ";"
    url = url[:-1]
    return InsecureClient(url, user=HDFS_USER_NAME)
