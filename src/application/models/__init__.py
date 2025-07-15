from sqlalchemy.orm import configure_mappers

from application.models.metadata_model import MetadataModel

from .base import Base
from .metadata_model import MetadataModel

configure_mappers()

__all__ = ["Base", "MetadataModel"]
