from uuid import UUID

from pydantic import BaseModel

from toolkit.types.urn import UploadURNType
from toolkit.types_ import UserID


class FavoriteQM(BaseModel):
    id: UUID
    user_id: UserID
    track_id: UploadURNType
