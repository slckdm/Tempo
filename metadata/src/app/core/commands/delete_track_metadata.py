from tempo_toolkit.application.outbox import OutboxMessage, OutboxService, OutboxStorage
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.contracts.events import MetadataDeletedEvent, UploadDeletedEvent
from tempo_toolkit.contracts.routing import METADATA_DELETED_EVENT_RK

from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.common.enums.aggregate_type import AggregateType
from app.core.common.services.metadata_service import MetadataService
from app.core.models.track_metadata import TrackMetadata


class DeleteTrackMetadata:
    def __init__(
        self,
        metadata_service: MetadataService,
        metadata_storage: MetadataStorage,
        object_storage: ObjectStorage,
        outbox_storage: OutboxStorage,
        outbox_service: OutboxService,
        transaction: Transaction,
        flusher: Flusher,
    ) -> None:
        self._metadata_service = metadata_service
        self._metadata_storage = metadata_storage
        self._object_storage = object_storage
        self._outbox_storage = outbox_storage
        self._outbox_service = outbox_service
        self._transaction = transaction
        self._flusher = flusher

    async def __call__(self, payload: UploadDeletedEvent) -> None:
        metadata = await self._metadata_storage.get_by_id(payload.upload_id.id, for_update=True)
        if not metadata:
            return

        if metadata.cover_key:
            await self._object_storage.delete_object(metadata.cover_key)
        await self._metadata_storage.delete(metadata)

        event = await self._create_notification(metadata, payload)
        await self._outbox_storage.add(event)

        await self._flusher.flush()
        await self._transaction.commit()

    async def _create_notification(
        self, metadata: TrackMetadata, payload: UploadDeletedEvent
    ) -> OutboxMessage:
        return await self._outbox_service.create_message(
            aggregate_type=AggregateType.METADATA,
            aggregate_id=str(metadata.upload_id),
            event_type=METADATA_DELETED_EVENT_RK,
            payload=MetadataDeletedEvent(upload_id=payload.upload_id),
        )
