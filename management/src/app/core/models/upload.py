"""Module: upload ORM model."""

from datetime import datetime

from tempo_toolkit.contracts.identifiers import UserID
from tempo_toolkit.contracts.uploads import UploadStatus, UploadURN

from app.core.common.types import UploadID


class Upload:

    def __init__(
        self,
        *,
        id: UploadID,
        filename: str,
        content_type: str,
        size: int,
        status: UploadStatus,
        created_by: UserID,
        created_at: datetime,
    ) -> None:
        self.id = id
        self.filename = filename
        self.content_type = content_type
        self.size = size
        self.status = status
        self.created_by = created_by
        self.created_at = created_at

    def __repr__(self) -> str:
        """StoredObject representation."""
        return f"{self.__class__.__name__}(id={self.id}, status={self.status})"

    @property
    def urn(self) -> UploadURN:
        return UploadURN(id=self.id)
