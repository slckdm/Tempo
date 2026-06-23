from typing import Annotated

from fastapi import Query

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from toolkit.service.response import JSendSuccessfulResponse

from app.core.commands.get_tracks_metadata import FilterParams, GetTracksMetadata
from app.core.schemas.dto.track_metadata_dto import TrackMetadataDTO
from app.core.schemas.response.tracks_metadata_response_body import (
    Pagination,
    TracksMetadataResponseBody,
)


@inject
async def get_tracks_metadata(
    interactor: FromDishka[GetTracksMetadata],
    filters: Annotated[FilterParams, Query()],
) -> JSendSuccessfulResponse[TracksMetadataResponseBody]:
    tracks_data = await interactor(filters)
    return JSendSuccessfulResponse(
        data=TracksMetadataResponseBody(
            metadata=[
                TrackMetadataDTO.model_validate(metadata) for metadata in tracks_data.metadata
            ],
            pagination=Pagination(
                offset=filters.offset, limit=filters.limit, total=tracks_data.total
            ),
        )
    )
