from dishka import FromDishka
from dishka.integrations.fastapi import inject

from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.queries.get_favorites import GetFavorites
from app.core.queries.models.favorites import FavoritesQM


@inject
async def get_favorites(
    interactor: FromDishka[GetFavorites]
) -> JSendSuccessfulResponse[FavoritesQM]:
    favorite = await interactor()
    return JSendSuccessfulResponse(data=favorite)
