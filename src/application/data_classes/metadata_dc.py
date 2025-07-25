import time
import uuid

from pydantic import BaseModel, ConfigDict, Field

from application.enums.allowed_extensions import AllowedExtensions
from application.enums.file_status import FileStatus
from application.enums.trip_types import TripTypes


class MetadataDC(BaseModel):
    file_name: str = ""
    file_type: AllowedExtensions = AllowedExtensions.CSV
    storage_path: str = ""
    storage_path_processed: str | None = None
    trip_type: TripTypes = None
    status: FileStatus = FileStatus.PENDING


class MetadataBaseDC(MetadataDC):
    file_metadata_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: int = Field(default_factory=lambda: int(time.time()))
    updated_at: int = Field(default_factory=lambda: int(time.time()))
    processed_at: int | None = None

    model_config = ConfigDict(from_attributes=True)
