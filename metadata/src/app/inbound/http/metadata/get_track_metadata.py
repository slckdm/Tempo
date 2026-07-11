
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from pydantic import BaseModel

from tempo_toolkit.contracts.uploads import UploadURN
from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.queries.get_track_metadata import GetTrackMetadata
from app.core.queries.models.metadata import MetadataQM


class MetadataResponse(BaseModel):
    metadata: MetadataQM


@inject
async def get_track_metadata(
    upload_id: UploadURN, interactor: FromDishka[GetTrackMetadata]
) -> JSendSuccessfulResponse[MetadataResponse]:
    track_metadata = await interactor(upload_id.id)
    return JSendSuccessfulResponse(data=MetadataResponse(metadata=track_metadata))
