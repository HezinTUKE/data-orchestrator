import os.path

from pyspark.sql import DataFrame

from application import spark
from application.aws.s3_manager import StorageManager
from application.data_classes.metadata_dc import MetadataBaseDC
from application.enums.allowed_extensions import AllowedExtensions
from application.spark.taxi_tripdata_schema import taxi_tripdata_schema


class StoreFileService:
    @classmethod
    async def upload_file(
        cls, file_content: bytes, file_name: str, file_path: str
    ) -> MetadataBaseDC | None:
        s3_manager = StorageManager()

        is_uploaded = s3_manager.upload_file(
            file_path=os.path.join(file_path, file_name), file_bytes=file_content
        )

        if not is_uploaded:
            return None

        extension = file_name.split(".")[-1].upper()

        return MetadataBaseDC(
            **{
                "file_name": file_name,
                "file_type": AllowedExtensions(extension),
                "storage_path": file_path,
            }
        )

    @classmethod
    async def read_file(
        cls, file_name: str, file_path: str, file_type: AllowedExtensions
    ) -> DataFrame:
        s3_manager = StorageManager()
        full_path = os.path.join(file_path, file_name)
        s3_bucket_path = f"s3a://{s3_manager.bucket.name}/{full_path}"
        if file_type == AllowedExtensions.PARQUET:
            parquet_content = spark.read.parquet(s3_bucket_path)
            res = spark.createDataFrame(
                parquet_content.rdd, schema=taxi_tripdata_schema
            )
        else:
            res = spark.read.csv(
                s3_bucket_path, header=True, schema=taxi_tripdata_schema
            )

        return res.fillna({
            "passenger_count": 0,
            "RatecodeID": 1,
            "store_and_fwd_flag": "N",
            "congestion_surcharge": 0.0,
            "Airport_fee": 0.0,
            "cbd_congestion_fee": 0.0
        })
