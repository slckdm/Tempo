from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, Enum, Float, Integer, String, Table

from toolkit.types.enum import UploadStatus

from app.core.models.track_metadata import TrackMetadata
from app.outbound.sqlalchemy.registry import mapper_registry

track_metadata_table = Table(
    "track_metadata",
    mapper_registry.metadata,
    Column("upload_id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("title", String, nullable=True),
    Column("artist", String, nullable=True),
    Column("album", String, nullable=True),
    Column("albumartist", String, nullable=True),
    Column("genre", String, nullable=True),
    Column("year", String, nullable=True),
    Column("track_number", Integer, nullable=True),
    Column("disc", Integer, nullable=True),
    Column("duration", Float, nullable=True),
    Column("bitrate", Float, nullable=True),
    Column("samplerate", Integer, nullable=True),
    Column("channels", Integer, nullable=True),
    Column("comment", String, nullable=True),
    Column("cover_key", String, nullable=True),
    Column("processing_status", Enum(UploadStatus), index=True, nullable=False),
    Column("error", String, nullable=True),
    Column("filename", String, nullable=False),
    Column("content_type", String, nullable=False),
    Column("size", Integer, nullable=False),
    Column("created_by", UUID, nullable=False),
    Column("created_at", DateTime(timezone=True), index=True, nullable=False),
    Column("origin_upload_status", Enum(UploadStatus), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)


def map_track_metadata_table() -> None:
    mapper_registry.map_imperatively(TrackMetadata, track_metadata_table)
