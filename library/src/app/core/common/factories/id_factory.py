from uuid import uuid4

from app.core.common.types import FavoriteID, PlaylistID, TrackID


def generate_favorite_id() -> FavoriteID:
    return FavoriteID(uuid4())


def generate_playlist_id() -> PlaylistID:
    return PlaylistID(uuid4())


def generate_track_id() -> TrackID:
    return TrackID(uuid4())
