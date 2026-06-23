from datetime import datetime
from uuid import UUID

from sqlalchemy import types as orm
from sqlalchemy.orm import Mapped, mapped_column

from toolkit.types.enum import UploadStatus
from toolkit.types.urn import UploadURNType

from .base import Base


class TrackMetadata(Base):
    __tablename__ = "track_metadata"

    upload_id: Mapped[UUID] = mapped_column(orm.UUID, primary_key=True)
    title: Mapped[str | None] = mapped_column(orm.String, nullable=True)
    artist: Mapped[str | None] = mapped_column(orm.String, nullable=True)
    album: Mapped[str | None] = mapped_column(orm.String, nullable=True)
    albumartist: Mapped[str | None] = mapped_column(orm.String, nullable=True)
    genre: Mapped[str | None] = mapped_column(orm.String, nullable=True)
    year: Mapped[str | None] = mapped_column(orm.String, nullable=True)
    track_number: Mapped[int | None] = mapped_column(orm.Integer, nullable=True)
    disc: Mapped[int | None] = mapped_column(orm.Integer, nullable=True)
    duration: Mapped[float | None] = mapped_column(orm.Float, nullable=True)
    bitrate: Mapped[float | None] = mapped_column(orm.Float, nullable=True)
    samplerate: Mapped[int | None] = mapped_column(orm.Integer, nullable=True)
    channels: Mapped[int | None] = mapped_column(orm.Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(orm.String, nullable=True)
    cover_key: Mapped[str | None] = mapped_column(orm.String, nullable=True)
    processing_status: Mapped[UploadStatus] = mapped_column(
        orm.Enum(UploadStatus), index=True
    )
    error: Mapped[str | None] = mapped_column(orm.String, nullable=True)
    filename: Mapped[str] = mapped_column(orm.String)
    content_type: Mapped[str] = mapped_column(orm.String)
    size: Mapped[int] = mapped_column(orm.Integer)
    created_by: Mapped[UUID] = mapped_column(orm.UUID)
    created_at: Mapped[datetime] = mapped_column(orm.DateTime(timezone=True), index=True)
    origin_upload_status: Mapped[UploadStatus] = mapped_column(orm.Enum(UploadStatus))
    updated_at: Mapped[datetime] = mapped_column(orm.DateTime(timezone=True))

    @property
    def urn(self) -> UploadURNType:
        return UploadURNType(id=self.upload_id)
