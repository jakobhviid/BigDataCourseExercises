FROM bde2020/spark-python-template:3.3.0-hadoop3.3

COPY example.py /app
#COPY example-solution.py /app

ENV SPARK_APPLICATION_PYTHON_LOCATION /app/example.py
#ENV SPARK_APPLICATION_PYTHON_LOCATION /app/example-solution.py
ENV SPARK_SUBMIT_ARGS "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0"
