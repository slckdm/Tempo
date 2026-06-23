from dishka import FromDishka
from dishka.integrations.fastapi import inject

from toolkit.service.response.response import JSendSuccessfulResponse
from toolkit.types.urn import UploadURNType

from app.core.commands.get_track_metadata import GetTrackMetadata
from app.core.schemas.dto.track_metadata_dto import TrackMetadataDTO
from app.core.schemas.response.track_metadata_response_body import TrackMetadataResponseBody


@inject
async def get_track_metadata(
    upload_id: UploadURNType, interactor: FromDishka[GetTrackMetadata]
) -> JSendSuccessfulResponse[TrackMetadataResponseBody]:
    track_metadata = await interactor(upload_id.id)
    return JSendSuccessfulResponse(
        data=TrackMetadataResponseBody(metadata=TrackMetadataDTO.model_validate(track_metadata))
    )
