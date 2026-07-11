from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, computed_field

from tempo_toolkit.contracts.identifiers import UserID
from tempo_toolkit.contracts.uploads import UploadStatus, UploadURN


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
    def urn(self) -> UploadURN:
        return UploadURN(self.id)
