
from pydantic import BaseModel

from app.core.schemas.dto.track_metadata_dto import TrackMetadataDTO


class Pagination(BaseModel):
    limit: int
    offset: int
    total: int


class TracksMetadataResponseBody(BaseModel):

    metadata: list[TrackMetadataDTO]
    pagination: Pagination
