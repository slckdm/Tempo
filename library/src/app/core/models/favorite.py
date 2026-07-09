"""Favorite ORM model."""

from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from toolkit.types_ import UserID

from .base import Base


class Favorite(Base):
    """Favorite model."""

    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "track_id", name="uq_favorites_user_id_track_id"),
    )

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    user_id: Mapped[UserID] = mapped_column()
    track_id: Mapped[str] = mapped_column()
