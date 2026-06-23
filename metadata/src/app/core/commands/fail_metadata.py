
from toolkit.messaging.contracts import MetadataFailedEvent, UploadCompletedEvent
from toolkit.messaging.routing import METADATA_FAILED_RK

from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.common.entities.metadata import Metadata
from app.core.common.enums import AggregateType
from app.core.common.services.metadata_service import MetadataService
from app.core.common.services.outbox_service import OutboxService


class FailMetadata:

    def __init__(
        self,
        flusher: Flusher,
        transaction: Transaction,
        outbox_storage: OutboxStorage,
        outbox_service: OutboxService,
        metadata_storage: MetadataStorage,
        metadata_service: MetadataService,
    ) -> None:
        self._flusher = flusher
        self._transaction = transaction
        self._outbox_service = outbox_service
        self._outbox_storage = outbox_storage
        self._metadata_storage = metadata_storage
        self._metadata_service = metadata_service

    async def __call__(self, payload: UploadCompletedEvent, exception: Exception) -> None:
        await self._transaction.rollback()

        metadata = await self._metadata_service.create(Metadata(), payload)
        await self._metadata_service.mark_failed(metadata, str(exception))

        message = await self._outbox_service.create_message(
            aggregate_type=AggregateType.UPLOAD,
            aggregate_id=str(payload.upload_id.id),
            event_type=METADATA_FAILED_RK,
            payload=MetadataFailedEvent(upload_id=payload.upload_id, reason=str(exception))
        )

        await self._metadata_storage.add(metadata)
        await self._outbox_storage.add(message)
        await self._flusher.flush()
        await self._transaction.commit()
