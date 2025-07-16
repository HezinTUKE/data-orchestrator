from pyspark.sql.types import (CharType, DataType, FloatType, IntegerType,
                               StructField, StructType)

taxi_tripdata_schema = StructType(
    [
        StructField("VendorID", IntegerType(), False),
        StructField("tpep_pickup_datetime", DataType(), False),
        StructField("tpep_dropoff_datetime", DataType(), False),
        StructField("passenger_count", IntegerType(), False),
        StructField("trip_distance", FloatType(), False),
        StructField("RatecodeID", IntegerType(), False),
        StructField("store_and_fwd_flag", CharType(1), False),
        StructField("PULocationID", IntegerType(), False),
        StructField("DOLocationID", IntegerType(), False),
        StructField("payment_type", IntegerType(), False),
        StructField("fare_amount", FloatType(), False),
        StructField("extra", FloatType(), False),
        StructField("mta_tax", FloatType(), False),
        StructField("tip_amount", FloatType(), False),
        StructField("tolls_amount", IntegerType(), False),
        StructField("improvement_surcharge", IntegerType(), False),
        StructField("total_amount", FloatType(), False),
        StructField("congestion_surcharge", FloatType(), False),
        StructField("Airport_fee", FloatType(), False),
        StructField("cbd_congestion_fee", FloatType(), True),
    ]
)
