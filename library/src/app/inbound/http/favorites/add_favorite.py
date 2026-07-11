from dishka import FromDishka
from dishka.integrations.fastapi import inject

from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.commands.add_favorite import AddFavorite, AddFavoriteRequest, AddFavoriteResponse


@inject
async def add_favorite(
    body: AddFavoriteRequest, interactor: FromDishka[AddFavorite]
) -> JSendSuccessfulResponse[AddFavoriteResponse]:
    favorite = await interactor(body)
    return JSendSuccessfulResponse(data=favorite)
