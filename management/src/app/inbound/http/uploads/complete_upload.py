"""Module: create upload endpoint."""

from dishka.integrations.fastapi import FromDishka, inject

from toolkit.service.response import JSendSuccessfulResponse
from toolkit.types.urn import UploadURNType

from app.core.commands.complete_upload import CompleteUpload


@inject
async def complete_upload(
    upload_id: UploadURNType, interactor: FromDishka[CompleteUpload]
) -> JSendSuccessfulResponse:
    """Create file upload."""
    await interactor(upload_id)
    return JSendSuccessfulResponse()
