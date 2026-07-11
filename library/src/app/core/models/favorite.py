"""Favorite ORM model."""

from tempo_toolkit.contracts.identifiers import UserID

from app.core.common.types import FavoriteID


class Favorite:
    """Favorite Track model."""

    def __init__(
        self,
        *,
        id: FavoriteID,
        user_id: UserID,
        track_id: str,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.track_id = track_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
