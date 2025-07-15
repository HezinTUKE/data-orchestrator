from io import BytesIO

import boto3
from boto3.s3.transfer import TransferConfig, TransferManager
from boto3.exceptions import S3UploadFailedError
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from application.config import get_config_section

CHUNK_SIZE = 50 * 1024 * 1024


class StorageManager:
    aws_config = get_config_section("aws")

    def __init__(self):
        self.s3_client: BaseClient = boto3.client("s3")
        bucket_name = f"""{self.aws_config.get("bucket_prefix")}-{self.aws_config.get("account_id")}"""

        if not self._check_bucket_exists(bucket_name=bucket_name, s3_client=self.s3_client):
            self.bucket = self.s3_client.create_bucket(
                Bucket=bucket_name, ACL="private", CreateBucketConfiguration={"LocationConstraint": self.aws_config.get("location")}
            )
        else:
            s3_resource = boto3.resource("s3")
            self.bucket = s3_resource.Bucket(bucket_name)

    def upload_file(self, file_path: str, file_bytes: bytes) -> bool:
        transfer_config = TransferConfig(multipart_threshold=CHUNK_SIZE, max_concurrency=10)
        transfer_manager = TransferManager(client=self.s3_client, config=transfer_config)
        try:
            transfer_manager.upload(BytesIO(file_bytes), bucket=self.bucket.name, key=file_path)
            return True
        except S3UploadFailedError as err:
            print(f"Couldn't upload file {file_path} to {self.bucket.name}.")
            print(f"\t{err}")
            return False

    def delete_file(self, file_path: str):
        try:
            self.s3_client.delete_object(Bucket=self.bucket.name, Key=file_path)
            return True
        except ClientError as err:
            print(f"Couldn't upload file {file_path} from bucket {self.bucket.name}.")
            print(f"\t{err}")
            return False

    @staticmethod
    def _check_bucket_exists(s3_client: BaseClient, bucket_name: str) -> bool:
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as ex:
            return False
