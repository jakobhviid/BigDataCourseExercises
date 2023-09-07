from pyspark import SparkConf, SparkContext
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()

# Limit cores to 1, and tell each executor to use one core = only one executor is used by Spark
conf = SparkConf().set('spark.executor.cores', 1).set('spark.cores.max',1).set('spark.executor.memory', '1g')
sc = SparkContext(master='spark://spark-master:7077', appName='myAppName', conf=conf)
# Filter function
select_words = lambda s : s[1] > 400

files = "hdfs://namenode:9000/stream-in/"
# Read in all files in the directory
txtFiles = sc.wholeTextFiles(files, 20)
# Take the content of the files and split them
all_word = txtFiles.flatMap(lambda s: s[1].split())
# Change from list of words to list of (word, 1)
word_map = all_word.map(lambda s: (s, 1))
# Merge values with equal keys
word_reduce = word_map.reduceByKey(lambda s, t: s+t)
# Filter using the defined lambda and sort by value
top_words = word_reduce.filter(select_words).sortBy(lambda s: s[1])
# Save as text file
top_words.saveAsTextFile('hdfs://namenode:9000/txt-out')
# Collect to a Python list and print
print(top_words.collect())

