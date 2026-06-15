"""Module: create upload endpoint."""

from dishka.integrations.fastapi import FromDishka, inject

from toolkit.service.response import JSendSuccessfulResponse

from app.core.commands.create_upload import CreateUpload
from app.schemas.request import CreateUploadRequestBody
from app.schemas.response import CreateUploadResponseBody


@inject
async def create_upload(
    body: CreateUploadRequestBody, interactor: FromDishka[CreateUpload]
) -> JSendSuccessfulResponse[CreateUploadResponseBody]:
    """Create file upload."""
    return await interactor.execute(body)
