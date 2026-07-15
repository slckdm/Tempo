"""Upload contracts."""

from enum import StrEnum
from uuid import UUID

from .identifiers import URN


class UploadStatus(StrEnum):
    """Upload processing status."""

    PENDING = "PENDING"
    PROCESSING_PENDING = "PROCESSING_PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED_PENDING = "COMPLETED_PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class UploadURN(URN[UUID]):
    """URN identifying an upload."""

    namespace = "mng.upload"
