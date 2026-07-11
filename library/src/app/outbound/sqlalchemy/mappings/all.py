from app.outbound.sqlalchemy.mappings.favorite import map_favorite_table
from app.outbound.sqlalchemy.mappings.playlist import map_playlists_table
from app.outbound.sqlalchemy.mappings.playlist_track import map_playlists_tracks_table
from app.outbound.sqlalchemy.registry import mapper_registry


def map_tables() -> None:
    if mapper_registry.mappers:
        return
    map_favorite_table()
    map_playlists_table()
    map_playlists_tracks_table()
