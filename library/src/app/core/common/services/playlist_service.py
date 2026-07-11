from toolkit.types_ import UserID

from app.core.common.factories.id_factory import generate_playlist_id
from app.core.models.playlist import Playlist
from app.core.models.playlist_track import PlaylistTrack


class PlaylistService:
    def create_playlist(self, user_id: UserID, name: str) -> Playlist:
        """Create a new playlist for the given user."""
        return Playlist(id=generate_playlist_id(), user_id=user_id, name=name)

    def add_track_to_playlist(self, playlist: Playlist, track: PlaylistTrack) -> None:
        """Add a track to the given playlist."""
        track.playlist_id = playlist.id
