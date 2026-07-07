from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from toolkit.types_ import UserID

from .base import Base

if TYPE_CHECKING:
    from app.core.models.playlist_track import PlaylistTrack


class Playlist(Base):
    """Playlist model."""

    __tablename__ = "playlists"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    user_id: Mapped[UserID] = mapped_column()
    name: Mapped[str] = mapped_column()

    tracks: Mapped[list["PlaylistTrack"]] = relationship(
        "PlaylistTrack",
        back_populates="playlist",
        lazy="raise",
        cascade="all,delete",
        primaryjoin="Playlist.id==PlaylistTrack.playlist_id",
    )
