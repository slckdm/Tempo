
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from pydantic import BaseModel

from toolkit.service.response import JSendSuccessfulResponse
from toolkit.types.urn import UploadURNType

from app.core.queries.get_track_metadata import GetTrackMetadata
from app.core.queries.models.metadata import MetadataQM


class MetadataResponse(BaseModel):
    metadata: MetadataQM


@inject
async def get_track_metadata(
    upload_id: UploadURNType, interactor: FromDishka[GetTrackMetadata]
) -> JSendSuccessfulResponse[MetadataResponse]:
    track_metadata = await interactor(upload_id.id)
    return JSendSuccessfulResponse(data=MetadataResponse(metadata=track_metadata))
