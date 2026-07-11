from toolkit.types_ import UserID

from app.core.common.types import PlaylistID


class Playlist:
    """Playlist model."""

    def __init__(
        self,
        *,
        id: PlaylistID,
        user_id: UserID,
        name: str,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.name = name
