import sys
from operator import add

from pyspark.sql import SparkSession

if len(sys.argv) != 2:
    print("Usage: wordcount <file>", file=sys.stderr)
    sys.exit(-1)

spark = SparkSession\
    .builder\
    .appName("PythonWordCount")\
    .getOrCreate()

# Read file line by line
lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
# Split each line at spaces (splits it into words)
words = lines.flatMap(lambda x: x.split(' '))
# Map each word to a tuple (word, 1)
tuples = words.map(lambda x: (x, 1))
# Reduce tuples by key (word) which results in a list of tuples with unique words and their total counts
sums = tuples.reduceByKey(add)
# Sort the list of tuples by the second element (count) in descending order
sorted = sums.sortBy(lambda x: x[1], ascending=False)

# Convert the sorted data to a DataFrame
result_df = sorted.toDF(schema=["word", "count"])

writer = result_df.write.mode("overwrite")

# Save the result to a JSON file
writer.json("s3a://spark-data/word-count-json")

# Save the result to a CSV file
writer.csv("s3a://spark-data/word-count-csv")

# Save the result to a Parquet file
writer.parquet("s3a://spark-data/word-count-parquet")

# Take the first 10 elements of the list
top_10 = sorted.take(10)
# Print the top 10 words and their counts
for (word, count) in top_10:
    print("%s: %i" % (word, count))

spark.stop()
