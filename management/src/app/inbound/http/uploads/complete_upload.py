"""Module: create upload endpoint."""

from dishka.integrations.fastapi import FromDishka, inject

from toolkit.service.response import JSendSuccessfulResponse

from app.core.commands.complete_upload import CompleteUpload
from app.core.common.types_ import UploadURNType
from app.core.schemas.response import CompleteUploadResponseBody


@inject
async def complete_upload(
    upload_id: UploadURNType, interactor: FromDishka[CompleteUpload]
) -> JSendSuccessfulResponse[CompleteUploadResponseBody]:
    """Create file upload."""
    return await interactor.execute(upload_id)
