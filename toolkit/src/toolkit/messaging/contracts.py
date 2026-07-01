from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from toolkit.types.enum import UploadStatus
from toolkit.types.urn import UploadURNType
from toolkit.types_ import UserID


class MessageContract(BaseModel):
    schema_version: int = 1

    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UploadCreatedEvent(MessageContract):
    upload_id: UploadURNType
    s3_key: str
    filename: str
    content_type: str
    size: int
    created_by: UserID
    created_at: datetime
    status: UploadStatus


class UploadCompletedEvent(MessageContract):
    upload_id: UploadURNType
    s3_key: str
    filename: str
    content_type: str
    size: int
    created_by: UserID
    created_at: datetime
    status: UploadStatus


class UploadDeletedEvent(MessageContract):
    upload_id: UploadURNType
    s3_key: str


class MetadataReadyEvent(MessageContract):
    upload_id: UploadURNType
    cover_key: str | None = None


class MetadataFailedEvent(MessageContract):
    upload_id: UploadURNType
    reason: str
