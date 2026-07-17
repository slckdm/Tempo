"""Healthcheck endpoint."""

from dishka.integrations.fastapi import FromDishka, inject

from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.commands.healthcheck import Healthcheck


@inject
async def healthcheck(
    interactor: FromDishka[Healthcheck],
) -> JSendSuccessfulResponse:
    """Return success when service dependencies are available."""
    await interactor()
    return JSendSuccessfulResponse()
