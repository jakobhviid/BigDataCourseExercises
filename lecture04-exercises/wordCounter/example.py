from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.functions import explode, split, to_json, array, col
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()

# Create SparkSession and configure it
spark = SparkSession.builder.appName('wordCount') \
    .config('spark.master','spark://spark-master:7077') \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '1g') \
    .config('spark.sql.streaming.checkpointLocation','hdfs://namenode:9000/stream-checkpoint/') \
    .getOrCreate()
    
# Create a read stream from Kafka and a topic
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "sentences") \
  .load()

# Cast to string
sentences = df.selectExpr("CAST(value AS STRING)")

# Split the sentences into words
# Note "explode" and "split" are SQL functions in Spark, not Python!
words = sentences.select(
   explode(
       split(sentences.value, " ")
   ).alias("word")
)

# Generate running word count by using SQL
wordCounts = words.groupBy("word").count().sort(col('count'))

# Only print words with more than 100 counts
filteredWordCounts = wordCounts.where('count > 100')

# Add a new column to our Dataframe, where the column name is "value" and the content is "(word, count)" as an SQL array
columns = [col('word'), col('count')]
mergedColumns = filteredWordCounts.withColumn('value', array(columns))

# Select the "mergedColumns.value" column, and convert to JSON with the alias "value", cast it to a string
# The "value" column is required by Kafka!
# Then create a Kafka write stream, with the output mode "complete"
mergedColumns.select(to_json(mergedColumns.value).alias('value')).selectExpr("CAST(value AS STRING)").writeStream \
    .format('kafka') \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("topic", "word-counts") \
    .outputMode("complete") \
    .start().awaitTermination()
