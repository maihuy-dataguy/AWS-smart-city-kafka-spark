from pyspark.sql.types import *
from pyspark.sql.functions import *

VEHICLE_SCHEMA = StructType([
    StructField("id", StringType(), True),
    StructField("device_id", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("location", StringType(), True),
    StructField("speed", DoubleType(), True),
    StructField("direction", StringType(), True),
    StructField("dealer", StringType(), True),
    StructField("model", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("fuelType", StringType(), True)
])

GPS_SCHEMA = StructType([
    StructField("id", StringType(), True),
    StructField("device_id", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("speed", DoubleType(), True),
    StructField("direction", StringType(), True),
    StructField("vehicle_type", StringType(), True)
])

TRAFFIC_SCHEMA = StructType([
    StructField("id", StringType(), True),
    StructField("device_id", StringType(), True),
    StructField("camera_id", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("location", StringType(), True),
    StructField("snapshot", StringType(), True)
])

WEATHER_SCHEMA = StructType([
    StructField("id", StringType(), True),
    StructField("device_id", StringType(), True),
    StructField("location", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("weather_condition", StringType(), True),
    StructField("precipitation", DoubleType(), True),
    StructField("wind_speed", DoubleType(), True),
    StructField("humidity", IntegerType(), True),
    StructField("air_quality_index", DoubleType(), True)
])

EMERGENCY_SCHEMA = StructType([
    StructField("id", StringType(), True),
    StructField("device_id", StringType(), True),
    StructField("incident_id", StringType(), True),
    StructField("type", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("location", StringType(), True),
    StructField("status", StringType(), True),
    StructField("description", StringType(), True)
])

