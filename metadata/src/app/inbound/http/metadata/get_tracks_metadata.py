from typing import Annotated

from fastapi import Query

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from pydantic import BaseModel, Field

from toolkit.service.response import JSendSuccessfulResponse

from app.core.queries.get_tracks_metadata import FilterParams, GetTracksMetadata, PaginationParams
from app.core.queries.models.list_metadata import ListMetadataQM


class ListMetadataRequestSchema(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=0, le=100)
    title: str | None = None
    artist: str | None = None
    album: str | None = None
    genre: str | None = None


@inject
async def get_tracks_metadata(
    interactor: FromDishka[GetTracksMetadata],
    query: Annotated[ListMetadataRequestSchema, Query()],
) -> JSendSuccessfulResponse[ListMetadataQM]:
    tracks_data = await interactor(
        FilterParams(
            title=query.title,
            artist=query.artist,
            album=query.album,
            genre=query.genre,
        ),
        PaginationParams(offset=query.offset, limit=query.limit),
    )
    return JSendSuccessfulResponse(data=tracks_data)
