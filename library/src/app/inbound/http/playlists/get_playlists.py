from typing import Annotated

from fastapi import Query

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from pydantic import BaseModel, Field

from toolkit.service.response import JSendSuccessfulResponse

from app.core.queries.get_playlists import GetPlaylists
from app.core.queries.models.playlists import PlaylistsQM
from app.core.queries.schemas.pagination import PaginationParams


class GetPlaylistsRequestSchema(BaseModel):
    offset: int = Field(0, le=50)
    limit: int = Field(50, ge=0)


@inject
async def get_playlists(
    query: Annotated[GetPlaylistsRequestSchema, Query()],
    interactor: FromDishka[GetPlaylists]
) -> JSendSuccessfulResponse[PlaylistsQM]:
    playlists = await interactor(
        pagination=PaginationParams(offset=query.offset, limit=query.limit)
    )

    return JSendSuccessfulResponse(data=playlists)
