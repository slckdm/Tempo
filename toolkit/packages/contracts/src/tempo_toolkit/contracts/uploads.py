"""Upload contracts."""

from enum import StrEnum
from uuid import UUID

from .identifiers import URN


class UploadStatus(StrEnum):
    """Upload processing status."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class UploadURN(URN[UUID]):
    """URN identifying an upload."""

    namespace = "mng.upload"
