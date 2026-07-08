from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.common.types import PlaylistID, TrackID

from .base import Base

if TYPE_CHECKING:
    from .playlist import Playlist


class PlaylistTrack(Base):
    """PlaylistTrack model."""

    __tablename__ = "playlist_tracks"

    id: Mapped[TrackID] = mapped_column(default=uuid4, primary_key=True)
    playlist_id: Mapped[PlaylistID] = mapped_column(ForeignKey("playlists.id"), nullable=False)
    track_id: Mapped[str] = mapped_column(nullable=False)

    playlist: Mapped["Playlist"] = relationship(
        "Playlist", foreign_keys=[playlist_id], back_populates="tracks", lazy="raise"
    )
