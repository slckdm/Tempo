"""Module: upload status enumeration."""

from enum import StrEnum


class UploadStatus(StrEnum):
    """Upload status enumeration."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
