from pydantic import BaseModel

from app.core.schemas.dto.track_metadata_dto import TrackMetadataDTO


class TrackMetadataResponseBody(BaseModel):

    metadata: TrackMetadataDTO
