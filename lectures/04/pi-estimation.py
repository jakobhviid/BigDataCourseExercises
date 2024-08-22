import locale
import sys
from operator import add
from random import random

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

locale.getdefaultlocale()
locale.getpreferredencoding()

# Limit cores to 1, and tell each executor to use one core = only one executor is used by Spark
conf = SparkConf().set('spark.executor.cores', 1).set('spark.cores.max',1).set('spark.executor.memory', '1g').set('spark.driver.host', '127.0.0.1')
sc = SparkContext(master='local', appName='pyspark-local', conf=conf)


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    # spark = SparkSession\
    #     .builder\
    #     .appName("PythonPi")\
    #     .getOrCreate()

    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = 100000 * partitions

    def f(_: int) -> float:
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = sc.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    # count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    print("Pi is roughly %f" % (4.0 * count / n))

    # spark.stop()
