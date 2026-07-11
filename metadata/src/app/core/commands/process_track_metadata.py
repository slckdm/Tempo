import asyncio
import io

from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.object_storage import ObjectStorage
from toolkit.common.ports.transaction import Transaction
from toolkit.messaging.contracts import MetadataReadyEvent, UploadCompletedEvent
from toolkit.messaging.routing import METADATA_READY_RK
from toolkit.outbox.model import OutboxMessage
from toolkit.outbox.ports.outbox_storage import OutboxStorage
from toolkit.outbox.service import OutboxService

from app.core.commands.ports.metadata_parser import MetadataParser
from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.common.enums import AggregateType
from app.core.common.exceptions import MetadataAlreadyProcessed
from app.core.common.services.metadata_service import MetadataService
from app.core.models.track_metadata import TrackMetadata

DEFAULT_COVER_MIMETYPE = "image/png"
COVER_KEY_FMT = "covers/{}"


class ProcessTrackMetadata:
    def __init__(
        self,
        metadata_service: MetadataService,
        metadata_storage: MetadataStorage,
        metadata_parser: MetadataParser,
        object_storage: ObjectStorage,
        outbox_storage: OutboxStorage,
        outbox_service: OutboxService,
        transaction: Transaction,
        flusher: Flusher,
    ) -> None:
        self._metadata_service = metadata_service
        self._metadata_storage = metadata_storage
        self._metadata_parser = metadata_parser
        self._transaction = transaction
        self._flusher = flusher
        self._object_storage = object_storage
        self._outbox_storage = outbox_storage
        self._outbox_service = outbox_service

    async def __call__(self, payload: UploadCompletedEvent) -> None:
        existing = await self._metadata_storage.get_by_id(payload.upload_id.id)

        if existing:
            raise MetadataAlreadyProcessed

        object_data = await self._object_storage.get_object(payload.s3_key)
        content = await asyncio.to_thread(object_data.body.read)
        object_data.body.close()
        raw = await self._metadata_parser.read(io.BytesIO(content))
        metadata = await self._metadata_service.create(raw, payload)

        if raw.cover:
            cover_key = COVER_KEY_FMT.format(payload.s3_key)
            params = {"ContentType": raw.cover.mime_type or DEFAULT_COVER_MIMETYPE}
            await self._object_storage.put_object(cover_key, body=raw.cover.data, **params)
            await self._metadata_service.update_cover_key(metadata, cover_key)

        await self._metadata_storage.add(metadata)
        event = await self._create_notification(metadata, payload)
        await self._outbox_storage.add(event)
        await self._flusher.flush()
        await self._transaction.commit()

    async def _create_notification(
        self, metadata: TrackMetadata, payload: UploadCompletedEvent
    ) -> OutboxMessage:
        return await self._outbox_service.create_message(
            aggregate_type=AggregateType.METADATA,
            aggregate_id=str(metadata.upload_id),
            event_type=METADATA_READY_RK,
            payload=MetadataReadyEvent(upload_id=payload.upload_id, cover_key=metadata.cover_key),
        )
