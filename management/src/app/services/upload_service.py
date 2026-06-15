from datetime import datetime, timezone
from http import HTTPStatus
from mimetypes import guess_type

from fastapi import HTTPException

from dishka import Provider

from toolkit.entities import User

from app.core.common.enums.upload_status import UploadStatus
from app.core.models.upload import Upload


class UploadService(Provider):

    def __init__(self) -> None:
        ...

    async def create_upload(
        self, filename: str, content_type: str, size: int, user: User
    ) -> Upload:

        mimetype, _ = guess_type(filename)

        if not mimetype or ("audio/" not in mimetype):
            raise HTTPException(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        upload = Upload(
            filename=filename,
            content_type=content_type,
            size=size,
            status=UploadStatus.PENDING,
            created_by=user.id,
            created_at=datetime.now(tz=timezone.utc),
        )

        return upload

    def list_uploads(self) -> ...: ...
