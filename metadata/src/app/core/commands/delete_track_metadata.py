from tempo_toolkit.application.outbox import OutboxService, OutboxStorage
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.contracts.events import UploadDeletedEvent

from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.common.services.metadata_service import MetadataService


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
