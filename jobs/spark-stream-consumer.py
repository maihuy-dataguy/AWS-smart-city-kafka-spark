from pyspark.sql import SparkSession

from jobs.config.config import configuration
from schema.smart_city_schema import *
from constants import *


def main():
    spark = SparkSession.builder.appName('Smart city streaming') \
        .config("spark.jar.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
                "org.apache.hadoop:hadoop-aws:3.3.1,"
                "com.amazonaws:aws-java-sdk:1.11.469") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.access.key", configuration.get("AWS_ACCESS_KEY")) \
        .config("spark.hadoop.fs.s3a.secret.key", configuration.get("AWS_SECRET_KEY")) \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider",
                'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider') \
        .getOrCreate()

    # Adjust the log level
    spark.sparkContext.setLogLevel("ERROR")

    def read_kafka_topic(topic, schema):
        return (spark.readStream.format("kafka")
                .option('kafka.bootstrap.servers', 'broker:29092')
                .option('subscribe', topic)
                .option('startingOffsets', 'earliest')
                .load()
                .selectExpr('CAST(value AS STRING)')
                .select(from_json(col('value'), schema).alias("data"))
                .select("data.*")
                .withWatermark('timestamp', '2 minutes')
                )

    def stream_writer(df: DataFrame, check_point_location, output):
        return (
            df.writeStream
                .format("parquet")
                .option("checkpointLocation", check_point_location)
                .option('path', output)
                .outputMode("append")
                .start()
        )

    vehicle_df = read_kafka_topic(VEHICLE_TOPIC, VEHICLE_SCHEMA).alias('vehicle')
    gps_df = read_kafka_topic(GPS_TOPIC, GPS_SCHEMA).alias('gps')
    traffic_df = read_kafka_topic(TRAFFIC_TOPIC, TRAFFIC_SCHEMA).alias('traffic')
    weather_df = read_kafka_topic(WEATHER_TOPIC, WEATHER_SCHEMA).alias('weather')
    emergency_df = read_kafka_topic(EMERGENCY_TOPIC, EMERGENCY_SCHEMA).alias('emergency')

    # Spark stream writer
    bucket_name = configuration.get("BUCKET_NAME")

    vehicle_sink = stream_writer(vehicle_df, f's3a://{bucket_name}/checkpoints/{VEHICLE_TOPIC}',
                                 f's3a://{bucket_name}/data/{VEHICLE_TOPIC}')
    gps_sink = stream_writer(gps_df, f's3a://{bucket_name}/checkpoints/{GPS_TOPIC}',
                             f's3a://{bucket_name}/data/{GPS_TOPIC}')
    traffic_sink = stream_writer(traffic_df, f's3a://{bucket_name}/checkpoints/{TRAFFIC_TOPIC}',
                                 f's3a://{bucket_name}/data/{TRAFFIC_TOPIC}')
    weather_sink = stream_writer(weather_df, f's3a://{bucket_name}/checkpoints/{WEATHER_TOPIC}',
                                 f's3a://{bucket_name}/data/{WEATHER_TOPIC}')
    emergency_sink = stream_writer(emergency_df, f's3a://{bucket_name}/checkpoints/{EMERGENCY_TOPIC}',
                                   f's3a://{bucket_name}/data/{EMERGENCY_TOPIC}')
    emergency_sink.awaitTermination()


if __name__ == '__main__':
    main()
