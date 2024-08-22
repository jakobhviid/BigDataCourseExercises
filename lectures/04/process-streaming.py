from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder.appName("Exercise 04").getOrCreate()

    streaming_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "INGESTION")
        .option("startingOffsets", "earliest")
        .load()
    )

    # TODO - create your logic
    # streaming_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    spark.stop()
