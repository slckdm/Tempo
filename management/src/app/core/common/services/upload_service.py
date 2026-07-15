from datetime import datetime, timezone
from mimetypes import guess_type

from tempo_toolkit.application.auth import User
from tempo_toolkit.application.errors import UnsupportedMediaType
from tempo_toolkit.application.outbox import OutboxService, OutboxStorage
from tempo_toolkit.contracts.routing import (
    UPLOAD_COMPLETED_EVENT_RK,
    UPLOAD_CREATED_EVENT_RK,
    UPLOAD_DELETED_EVENT_RK,
)
from tempo_toolkit.contracts.uploads import UploadStatus

from app.core.common.enums.aggregate_type import AggregateType
from app.core.common.exceptions import StatusUpdateFlowError
from app.core.common.factories.id_factory import generate_upload_id
from app.core.common.factories.message_factorites import (
    make_upload_completed_message,
    make_upload_created_message,
    make_upload_deleted_message,
)
from app.core.models.upload import Upload


class UploadService:
    def __init__(
        self,
        outbox_service: OutboxService,
        outbox_storage: OutboxStorage,
    ) -> None:
        self._outbox_service = outbox_service
        self._outbox_storage = outbox_storage

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

    async def complete_upload(self, upload: Upload) -> None:
        await self.transit_status(upload, UploadStatus.PROCESSING)

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

    async def make_upload_completed_event(self, upload: Upload) -> None:
        message = await self._outbox_service.create_message(
            aggregate_type=AggregateType.UPLOAD,
            aggregate_id=str(upload.id),
            event_type=UPLOAD_COMPLETED_EVENT_RK,
            payload=make_upload_completed_message(upload),
        )
        await self._outbox_storage.add(message)

    async def make_upload_created_event(self, upload: Upload) -> None:
        message = await self._outbox_service.create_message(
            aggregate_type=AggregateType.UPLOAD,
            aggregate_id=str(upload.id),
            event_type=UPLOAD_CREATED_EVENT_RK,
            payload=make_upload_created_message(upload),
        )
        await self._outbox_storage.add(message)

    async def make_upload_deleted_event(self, upload: Upload) -> None:
        message = await self._outbox_service.create_message(
            aggregate_type=AggregateType.UPLOAD,
            aggregate_id=str(upload.id),
            event_type=UPLOAD_DELETED_EVENT_RK,
            payload=make_upload_deleted_message(upload),
        )
        await self._outbox_storage.add(message)

    def list_uploads(self) -> ...: ...
