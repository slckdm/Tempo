from app.core.common.types import PlaylistID, TrackID


class PlaylistTrack:
    """PlaylistTrack model."""

    def __init__(
        self,
        *,
        id: TrackID,
        playlist_id: PlaylistID,
        track_id: str,
    ) -> None:
        self.id = id
        self.playlist_id = playlist_id
        self.track_id = track_id
