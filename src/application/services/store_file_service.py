import os.path

from application.aws.s3_manager import StorageManager
from application.data_classes.metadata_dc import MetadataBaseDC
from application.enums.allowed_extensions import AllowedExtensions


class StoreFileService:
    @classmethod
    async def upload_file(cls, file_content: bytes, file_name: str, file_path: str) -> MetadataBaseDC | None:
        s3_manager = StorageManager()

        is_uploaded = s3_manager.upload_file(file_path=os.path.join(file_path, file_name), file_bytes=file_content)

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
