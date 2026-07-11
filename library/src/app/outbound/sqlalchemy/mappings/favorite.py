from uuid import uuid4

from sqlalchemy import UUID, Column, String, Table, UniqueConstraint

from app.core.models.favorite import Favorite
from app.outbound.sqlalchemy.registry import mapper_registry

favorite_table = Table(
    "favorites",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), default=uuid4, primary_key=True, nullable=False),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    Column("track_id", String, nullable=False),
    UniqueConstraint("user_id", "track_id", name="uq_favorites_user_id_track_id"),

)


def map_favorite_table() -> None:
    mapper_registry.map_imperatively(Favorite, favorite_table)
