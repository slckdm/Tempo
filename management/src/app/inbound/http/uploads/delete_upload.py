"""Module: delete upload endpoint."""

from dishka.integrations.fastapi import FromDishka, inject

from tempo_toolkit.contracts.uploads import UploadURN
from tempo_toolkit.infrastructure.web import JSendSuccessfulResponse

from app.core.commands.delete_upload import DeleteUpload


@inject
async def delete_upload(
    upload_id: UploadURN, interactor: FromDishka[DeleteUpload]
) -> JSendSuccessfulResponse:
    """Delete upload."""
    await interactor(upload_id)
    return JSendSuccessfulResponse()
