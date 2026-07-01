"""Module: delete upload endpoint."""

from dishka.integrations.fastapi import FromDishka, inject
from toolkit.service.response import JSendSuccessfulResponse
from toolkit.types.urn import UploadURNType

from app.core.commands.delete_upload import DeleteUpload


@inject
async def delete_upload(
    upload_id: UploadURNType, interactor: FromDishka[DeleteUpload]
) -> JSendSuccessfulResponse:
    """Delete upload."""
    await interactor(upload_id)
    return JSendSuccessfulResponse()
