
from app.core.models.playlist_track import PlaylistTrack


class PlaylistTrackService:

    def create_track(self, track_id: str) -> PlaylistTrack:
        """Create a new track for the given user."""
        return PlaylistTrack(track_id=track_id)
