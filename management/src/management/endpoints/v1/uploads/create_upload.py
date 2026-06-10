"""Module: create upload endpoint."""

from datetime import datetime, timezone
from http import HTTPStatus
from mimetypes import guess_type
from typing import Annotated

from fastapi import Depends, Request
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from toolkit.security.models import User
from toolkit.service.response import JSendSuccessfulResponse

from management.common.clients import s3_client
from management.common.enums import UploadStatus
from management.common.utils import get_current_user
from management.core.configs import S3Config
from management.core.db import get_db_session
from management.models import Upload
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
    presigned_url = s3_client.generate_presigned_url(
        S3Config.bucket, body.filename, content_type=body.content_type
    )
    mimetype, _ = guess_type(body.filename)

    if not mimetype or ("audio/" not in mimetype):
        raise HTTPException(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    async with db() as db_session:
        upload = Upload(
            filename=body.filename,
            content_type=body.content_type,
            size=body.size,
            status=UploadStatus.PENDING,
            created_by=user.id,
            created_at=datetime.now(tz=timezone.utc)
        )
        db_session.add(upload)
        await db_session.commit()
        await db_session.refresh(upload)

    return JSendSuccessfulResponse(
        data=CreateUploadResponseBody(
            upload=UploadDTO(urn=f"urn:management.upload:{upload.id}"),
            presigned_url=presigned_url,
        )
    )
