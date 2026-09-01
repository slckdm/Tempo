"""Cross-service event contracts."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .identifiers import UserID
from .uploads import UploadStatus, UploadURN


class EventContract(BaseModel):
    """Base event envelope."""

    schema_version: int = 1
    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UploadCreatedEvent(EventContract):
    """Upload-created event."""

    upload_id: UploadURN
    s3_key: str
    filename: str
    content_type: str
    size: int
    created_by: UserID
    created_at: datetime
    status: UploadStatus


class UploadCompletedEvent(EventContract):
    """Upload-completed event."""

    upload_id: UploadURN
    s3_key: str
    filename: str
    content_type: str
    size: int
    created_by: UserID
    created_at: datetime
    status: UploadStatus


class UploadDeletedEvent(EventContract):
    """Upload-deleted event."""

    upload_id: UploadURN
    s3_key: str


class MetadataReadyEvent(EventContract):
    """Metadata-ready event."""

    upload_id: UploadURN
    cover_key: str | None = None
    title: str | None = None
    artist: str | None = None
    album: str | None = None
    genre: str | None = None
    year: str | None = None
    content_type: str | None = None


class MetadataDeletedEvent(EventContract):
    """Metadata-deleted event."""

    upload_id: UploadURN


class MetadataFailedEvent(EventContract):
    """Metadata-failed event."""

    upload_id: UploadURN
    reason: str


class FeatureReadyEvent(EventContract):
    """Feature-ready event."""

    upload_id: UploadURN
