from enum import StrEnum


class UploadStatus(StrEnum):
    """Upload status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
