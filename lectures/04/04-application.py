from pyspark.sql import SparkSession

if __name__ == "__main__":
    # import os

    # os.environ[
    #     "SPARK_SUBMIT_ARGS"
    # ] = "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0"

    spark = SparkSession.builder.appName("Exercise 04 - TODO").getOrCreate()

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "strimzi-kafka-bootstrap.kafka:9092")
        .option("subscribe", "INGESTION")
        .option("startingOffsets", "earliest")
        .load()
    )
    print("SPARK - ready")

    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    print("SPARK - done")
    print(df)

    spark.stop()
