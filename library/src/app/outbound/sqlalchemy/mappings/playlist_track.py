from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey, String, Table, UniqueConstraint

from app.core.models.playlist_track import PlaylistTrack
from app.outbound.sqlalchemy.registry import mapper_registry

playlists_tracks_table = Table(
    "playlist_tracks",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), default=uuid4, primary_key=True),
    Column("playlist_id", UUID(as_uuid=True), ForeignKey("playlists.id"), nullable=False),
    Column("track_id", String, nullable=False),
    UniqueConstraint("playlist_id", "track_id", name="uq_playlist_tracks_playlist_id_track_id"),
)


def map_playlists_tracks_table() -> None:
    mapper_registry.map_imperatively(PlaylistTrack, playlists_tracks_table)
