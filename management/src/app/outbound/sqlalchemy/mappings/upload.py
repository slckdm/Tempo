from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, Enum, Integer, String, Table

from tempo_toolkit.contracts.uploads import UploadStatus

from app.core.models.upload import Upload
from app.outbound.sqlalchemy.registry import mapper_registry

upload_table = Table(
    "uploads",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("filename", String, nullable=False),
    Column("content_type", String, nullable=False),
    Column("size", Integer, nullable=False),
    Column("status", Enum(UploadStatus), default=UploadStatus.PENDING, nullable=False),
    Column("created_by", UUID, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)


def map_uploads_table() -> None:
    mapper_registry.map_imperatively(Upload, upload_table)
