from pydantic import BaseModel

from app.core.queries.models.playlist import PlaylistQM


class PlaylistsQM(BaseModel):
    playlists: list[PlaylistQM]
    total: int
    limit: int
    offset: int
