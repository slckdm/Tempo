"""Module: complete upload endpoint."""

from dishka.integrations.fastapi import FromDishka, inject

from tempo_toolkit.contracts.uploads import UploadURN
from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.commands.complete_upload import CompleteUpload


@inject
async def complete_upload(
    upload_id: UploadURN, interactor: FromDishka[CompleteUpload]
) -> JSendSuccessfulResponse:
    """Complete upload."""
    await interactor(upload_id)
    return JSendSuccessfulResponse()
