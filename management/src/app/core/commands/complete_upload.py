from toolkit.messaging.contracts import UploadCompletedEvent
from toolkit.messaging.routing import UPLOAD_COMPLETED_RK
from toolkit.service.exceptions import NotFound
from toolkit.types.enum import UploadStatus
from toolkit.types.urn import UploadURNType

from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.object_storage import ObjectStorage
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.enums.aggregate_type import AggregateType
from app.core.common.services import CurrentUserService, OutboxService, UploadService


class CompleteUpload:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        upload_service: UploadService,
        upload_storage: UploadStorage,
        outbox_service: OutboxService,
        outbox_storage: OutboxStorage,
        object_storage: ObjectStorage,
        transaction: Transaction,
        flusher: Flusher,
    ) -> None:
        self._current_user_service = current_user_service
        self._upload_service = upload_service
        self._upload_storage = upload_storage
        self._outbox_service = outbox_service
        self._outbox_storage = outbox_storage
        self._object_storage = object_storage
        self._transaction = transaction
        self._flusher = flusher

    async def __call__(
        self, upload_id: UploadURNType
    ) -> None:
        await self._current_user_service.get_current_user()
        upload = await self._upload_storage.get_by_id(upload_id.id, for_update=True)

        if not upload:
            raise NotFound(data={"upload": upload_id})

        await self._object_storage.get_object(str(upload.urn))
        await self._upload_service.transit_status(upload, UploadStatus.PROCESSING)
        message = await self._outbox_service.create_message(
            aggregate_type=AggregateType.UPLOAD,
            aggregate_id=str(upload.id),
            event_type=UPLOAD_COMPLETED_RK,
            payload=UploadCompletedEvent(
                upload_id=upload.urn,
                s3_key=str(upload.urn),
                filename=upload.filename,
                content_type=upload.content_type,
                size=upload.size,
                created_by=upload.created_by,
                created_at=upload.created_at,
                status=upload.status
            ),
        )
        await self._outbox_storage.add(message)

        await self._flusher.flush()
        await self._transaction.commit()
