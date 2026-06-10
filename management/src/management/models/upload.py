"""Module: upload ORM model."""

from datetime import datetime

from sqlalchemy import types
from sqlalchemy.orm import Mapped, mapped_column

from management.common.enums import UploadStatus

from .base import Base


class Upload(Base):
    """Upload ORM Model."""

    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(types.Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(types.String, nullable=False)
    content_type: Mapped[str] = mapped_column(types.String, nullable=False)
    size: Mapped[int] = mapped_column(types.Integer, nullable=False)
    # external_key: Mapped[str] = mapped_column(types.String, unique=True, nullable=False)
    status: Mapped[UploadStatus] = mapped_column(
        types.Enum(UploadStatus), default=UploadStatus.PENDING, nullable=False
    )
    created_by: Mapped[str] = mapped_column(types.String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(types.DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        """Object representation."""
        return f"{self.__class__.__name__}(id={self.id}, status={self.status})"
