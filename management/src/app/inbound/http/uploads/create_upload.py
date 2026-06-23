"""Module: create upload endpoint."""

from dishka.integrations.fastapi import FromDishka, inject

from toolkit.service.response import JSendSuccessfulResponse

from app.core.commands.create_upload import CreateUpload
from app.core.schemas.dto import UploadDTO
from app.core.schemas.request import CreateUploadRequestBody
from app.core.schemas.response import CreateUploadResponseBody


@inject
async def create_upload(
    body: CreateUploadRequestBody, interactor: FromDishka[CreateUpload]
) -> JSendSuccessfulResponse[CreateUploadResponseBody]:
    """Create file upload."""
    upload_data = await interactor(body)
    return JSendSuccessfulResponse(
        data=CreateUploadResponseBody(
            upload=UploadDTO(urn=upload_data.upload.urn),
            presigned_url=upload_data.presigned_url,
        )
    )
