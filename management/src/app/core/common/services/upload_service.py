from datetime import datetime, timezone
from mimetypes import guess_type

from tempo_toolkit.application.auth import User
from tempo_toolkit.application.errors import UnsupportedMediaType
from tempo_toolkit.contracts.uploads import UploadStatus

from app.core.common.exceptions import StatusUpdateFlowError
from app.core.common.factories.id_factory import generate_upload_id
from app.core.models.upload import Upload


class UploadService:

    def __init__(self): ...

    async def create_upload(
        self, filename: str, size: int, user: User
    ) -> Upload:
        mimetype, _ = guess_type(filename)

        if not mimetype or ("audio/" not in mimetype):
            raise UnsupportedMediaType

        upload = Upload(
            id=generate_upload_id(),
            filename=filename,
            content_type=mimetype,
            size=size,
            status=UploadStatus.PENDING,
            created_by=user.id,
            created_at=datetime.now(tz=timezone.utc),
        )

        return upload

    async def transit_status(self, upload: Upload, status: UploadStatus) -> None:
        TRANSITIONS_MAP = {
            UploadStatus.PROCESSING: (UploadStatus.PENDING,),
            UploadStatus.COMPLETED: (UploadStatus.PROCESSING,),
            UploadStatus.FAILED: (UploadStatus.PENDING, UploadStatus.PROCESSING),
        }
        allowed_transitions = TRANSITIONS_MAP[status]
        if upload.status in allowed_transitions:
            upload.status = status
        else:
            raise StatusUpdateFlowError

    def list_uploads(self) -> ...: ...
