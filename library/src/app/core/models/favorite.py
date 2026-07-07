from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from toolkit.types_ import UserID

from .base import Base


class Favorite(Base):
    """Favorite model."""

    __tablename__ = "favorites"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    user_id: Mapped[UserID] = mapped_column()
    track_id: Mapped[str] = mapped_column()
