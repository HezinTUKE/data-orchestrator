import time
import uuid

from sqlalchemy import UUID, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from application.enums.allowed_extensions import AllowedExtensions
from application.enums.file_status import FileStatus
from application.models.base import Base


class MetadataModel(Base):
    __tablename__ = "file_metadata"

    file_metadata_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: uuid.uuid4()
    )
    file_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    file_type: Mapped[AllowedExtensions] = mapped_column(
        Enum(AllowedExtensions), index=True, nullable=False
    )
    storage_path: Mapped[str] = mapped_column(String, nullable=False, index=True)
    storage_path_processed: Mapped[str] = mapped_column(
        String, nullable=True, index=True
    )
    status: Mapped[FileStatus] = mapped_column(
        Enum(FileStatus), nullable=False, default=FileStatus.PENDING, index=True
    )
    created_at: Mapped[int] = mapped_column(Integer, default=lambda: int(time.time()))
    updated_at: Mapped[int] = mapped_column(
        Integer, default=lambda: int(time.time()), onupdate=lambda: int(time.time())
    )
    processed_at: Mapped[int] = mapped_column(Integer, nullable=True)
