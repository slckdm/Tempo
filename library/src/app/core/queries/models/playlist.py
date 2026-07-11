from uuid import UUID

from pydantic import BaseModel

from tempo_toolkit.contracts.identifiers import UserID


class PlaylistQM(BaseModel):
    id: UUID
    user_id: UserID
    name: str
    tracks_count: int
