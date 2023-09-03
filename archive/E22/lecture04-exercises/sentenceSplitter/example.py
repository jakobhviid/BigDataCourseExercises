# Remember last time? It was called SparkContext there, however, another Spark instance is required to do streaming
# from pyspark import SparkConf, SparkContext

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()

files = "hdfs://namenode:9000/stream-in/"

# Start a SparkSession, and configure it like last time
spark = SparkSession.builder.appName('sentenceSplitter') \
    .config('spark.master','spark://spark-master:7077') \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://namenode:9000/stream-checkpoint/') \
    .getOrCreate()

# Create a read stream, define the path and what seperator to use. 
# Tell the seperator to be ".", and then use "text" to read in text files
df = spark.readStream.option('lineSep','.').text(files)
# Another way to do it, but it will not split by ".", but by line separators
# schema = StructType().add("value", "string")
# df = spark.readStream.option('path',files).schema(schema).format('text').load()

# Cast the stream's column "value" as string.
# Create a Kafka write stream and define the require parameters.
# Start it, and await termination.
df.selectExpr("CAST(value AS STRING)").writeStream \
    .format('kafka') \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("topic", "sentences") \
    .outputMode("append") \
    .start().awaitTermination()
