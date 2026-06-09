"""Module: create upload endpoint."""

from typing import Annotated

from fastapi import Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from toolkit.response import JSendSuccessfulResponse
from toolkit.security.models import User

from management.common.clients import s3_client
from management.common.utils import get_current_user
from management.core.configs import S3Config
from management.core.service import get_db_session
from management.schemas.dto import UploadDTO
from management.schemas.request import CreateUploadRequestBody
from management.schemas.response import CreateUploadResponseBody


async def create_upload(
    request: Request,
    body: CreateUploadRequestBody,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[async_sessionmaker[AsyncSession], Depends(get_db_session)],
) -> JSendSuccessfulResponse[CreateUploadResponseBody]:
    """Create file upload."""
    presigned_url = s3_client.generate_presigned_url(S3Config.bucket, body.filename)
    async with db() as db_session:
        db_session

    response_body = CreateUploadResponseBody(
        upload=UploadDTO(urn="123e4567-e89b-12d3-a456-426614174000")
    )
    return JSendSuccessfulResponse(data=response_body)
