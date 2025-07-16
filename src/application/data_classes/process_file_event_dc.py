from pydantic import BaseModel, Field


class ProcessFileEventDC(BaseModel):
    file_metadata_ids: list[str] = Field(default_factory=list)
