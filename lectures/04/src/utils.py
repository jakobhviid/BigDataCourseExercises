
import locale
from pyspark import SparkConf, SparkContext

locale.getdefaultlocale()
locale.getpreferredencoding()


# Limit cores to 1, and tell each executor to use one core = only one executor is used by Spark


def get_spark_context(master:str, app_name:str, config: dict) -> SparkContext:
    conf = SparkConf().setAll(config)
    # .set("spark.executor.cores", 
    #                        config.get('spark.executor.cores', 1)).set("spark.cores.max",
    #                                                                   config.get('spark.cores.max',1)).set("spark.executor.memory",
    #                                                                                                        config.get('spark.executor.memory', '1g'))
    return SparkContext(master=master, appName=app_name, conf=conf)