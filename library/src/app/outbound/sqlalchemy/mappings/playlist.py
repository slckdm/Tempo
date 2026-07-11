from uuid import uuid4

from sqlalchemy import UUID, Column, String, Table

from app.core.models.playlist import Playlist
from app.outbound.sqlalchemy.registry import mapper_registry

playlists_table = Table(
    "playlists",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), default=uuid4, primary_key=True),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    Column("name", String, nullable=False),
)


def map_playlists_table() -> None:
    mapper_registry.map_imperatively(Playlist, playlists_table)
