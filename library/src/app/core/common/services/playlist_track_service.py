from app.core.common.factories.id_factory import generate_track_id
from app.core.common.types import PlaylistID
from app.core.models.playlist_track import PlaylistTrack


class PlaylistTrackService:
    def create_track(self, playlist_id: PlaylistID, track_id: str) -> PlaylistTrack:
        """Create a new track for the given user."""
        return PlaylistTrack(id=generate_track_id(), playlist_id=playlist_id, track_id=track_id)
