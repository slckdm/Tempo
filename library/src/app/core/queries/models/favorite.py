from uuid import UUID

from pydantic import BaseModel

from tempo_toolkit.contracts.identifiers import UserID
from tempo_toolkit.contracts.uploads import UploadURN


class FavoriteQM(BaseModel):
    id: UUID
    user_id: UserID
    track_id: UploadURN
