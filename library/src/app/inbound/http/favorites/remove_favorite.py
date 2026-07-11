from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.commands.remove_favorite import RemoveFavorite


@inject
async def remove_favorite(
    favorite_id: UUID,
    interactor: FromDishka[RemoveFavorite]
) -> JSendSuccessfulResponse:
    await interactor(favorite_id)
    return JSendSuccessfulResponse()
