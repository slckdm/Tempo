from datetime import datetime, timezone
from http import HTTPStatus
from mimetypes import guess_type

from fastapi import HTTPException

from dishka import Provider

from toolkit.entities import User

from app.core.common.enums.upload_status import UploadStatus
from app.core.common.exceptions import BaseError
from app.core.models.upload import Upload


class UploadAlreadyFinished(BaseError):
    default_message = "Upload already has been completed"



class UploadService(Provider):

    def __init__(self): ...

    async def create_upload(self, filename: str, size: int, user: User) -> Upload:
        mimetype, _ = guess_type(filename)

        if not mimetype or ("audio/" not in mimetype):
            raise HTTPException(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        upload = Upload(
            filename=filename,
            content_type=mimetype,
            size=size,
            status=UploadStatus.PENDING,
            created_by=user.id,
            created_at=datetime.now(tz=timezone.utc),
        )

        return upload

    async def complete_upload(self, upload: Upload) -> None:
        if upload.status == UploadStatus.PENDING:
            upload.status = UploadStatus.COMPLETED
        else:
            raise UploadAlreadyFinished

    def list_uploads(self) -> ...: ...
