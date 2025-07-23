from pyspark.sql.types import (
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

taxi_tripdata_schema = StructType(
    [
        StructField("VendorID", IntegerType(), False),
        StructField("tpep_pickup_datetime", TimestampType(), False),
        StructField("tpep_dropoff_datetime", TimestampType(), False),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", FloatType(), False),
        StructField("RatecodeID", IntegerType(), True),
        StructField("store_and_fwd_flag", StringType(), True),
        StructField("PULocationID", IntegerType(), False),
        StructField("DOLocationID", IntegerType(), False),
        StructField("payment_type", IntegerType(), False),
        StructField("fare_amount", FloatType(), False),
        StructField("extra", FloatType(), False),
        StructField("mta_tax", FloatType(), False),
        StructField("tip_amount", FloatType(), False),
        StructField("tolls_amount", FloatType(), False),
        StructField("improvement_surcharge", FloatType(), False),
        StructField("total_amount", FloatType(), False),
        StructField("congestion_surcharge", FloatType(), True),
        StructField("Airport_fee", FloatType(), True),
        StructField("cbd_congestion_fee", FloatType(), True),
    ]
)
