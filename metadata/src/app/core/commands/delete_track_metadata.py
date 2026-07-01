from toolkit.messaging.contracts import UploadDeletedEvent

from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.commands.ports.object_storage import ObjectStorage
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.common.services.metadata_service import MetadataService
from app.core.common.services.outbox_service import OutboxService


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

        await self._flusher.flush()
        await self._transaction.commit()
