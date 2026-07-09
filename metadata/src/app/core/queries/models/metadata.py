from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, computed_field

from toolkit.types.enum import UploadStatus
from toolkit.types.urn import UploadURNType
from toolkit.types_ import UserID


class MetadataQM(BaseModel):
    id: UUID = Field(exclude=True)
    filename: str
    content_type: str
    processing_status: UploadStatus
    title: str | None
    artist: str | None
    album: str | None
    genre: str | None
    year: str | None
    duration: float | None
    cover_key: str | None
    size: int
    created_at: datetime
    created_by: UserID

    @computed_field
    @property
    def urn(self) -> UploadURNType:
        return UploadURNType(self.id)
