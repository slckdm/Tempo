"""Module: create upload endpoint."""

from dishka.integrations.fastapi import FromDishka, inject
from toolkit.service.response import JSendSuccessfulResponse

from app.core.commands.create_upload import (
    CreateUpload,
    CreateUploadRequestBody,
    CreateUploadResponse,
)


@inject
async def create_upload(
    body: CreateUploadRequestBody, interactor: FromDishka[CreateUpload]
) -> JSendSuccessfulResponse[CreateUploadResponse]:
    """Create upload."""
    upload_data = await interactor(body)
    return JSendSuccessfulResponse(data=upload_data)
