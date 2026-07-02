import pytest

from app.core.commands.delete_track_metadata import DeleteTrackMetadata
from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.commands.ports.object_storage import ObjectStorage
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.common.ports.utc_timer import UTCTimer
from app.core.common.services.metadata_service import MetadataService
from app.core.common.services.outbox_service import OutboxService
from tests.unit.core.factories import (
    create_metadata_service,
    create_outbox_service,
    create_track_metadata,
    create_upload_deleted_event,
)


def make_delete_track_metadata_command(
    metadata_service: MetadataService,
    metadata_storage: MetadataStorage,
    object_storage: ObjectStorage,
    outbox_storage: OutboxStorage,
    outbox_service: OutboxService,
    transaction: Transaction,
    flusher: Flusher,
) -> DeleteTrackMetadata:
    return DeleteTrackMetadata(
        metadata_service=metadata_service,
        metadata_storage=metadata_storage,
        object_storage=object_storage,
        outbox_storage=outbox_storage,
        outbox_service=outbox_service,
        transaction=transaction,
        flusher=flusher,
    )


@pytest.mark.asyncio
async def test_delete_track_metadata_with_cover(
    utc_timer: UTCTimer,
    metadata_storage: MetadataStorage,
    object_storage: ObjectStorage,
    outbox_storage: OutboxStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    metadata = create_track_metadata(cover_key="covers/some-key")
    metadata_storage.get_by_id.return_value = metadata
    event = create_upload_deleted_event()
    command = make_delete_track_metadata_command(
        metadata_service=create_metadata_service(utc_timer),
        outbox_service=create_outbox_service(utc_timer),
        metadata_storage=metadata_storage,
        object_storage=object_storage,
        outbox_storage=outbox_storage,
        flusher=flusher,
        transaction=transaction,
    )

    await command(event)

    metadata_storage.get_by_id.assert_called_once_with(event.upload_id.id, for_update=True)
    object_storage.delete_object.assert_called_once_with("covers/some-key")
    metadata_storage.delete.assert_called_once_with(metadata)
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_track_metadata_without_cover(
    utc_timer: UTCTimer,
    metadata_storage: MetadataStorage,
    object_storage: ObjectStorage,
    outbox_storage: OutboxStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    metadata = create_track_metadata(cover_key=None)
    metadata_storage.get_by_id.return_value = metadata
    event = create_upload_deleted_event()
    command = make_delete_track_metadata_command(
        metadata_service=create_metadata_service(utc_timer),
        outbox_service=create_outbox_service(utc_timer),
        metadata_storage=metadata_storage,
        object_storage=object_storage,
        outbox_storage=outbox_storage,
        flusher=flusher,
        transaction=transaction,
    )

    await command(event)

    object_storage.delete_object.assert_not_called()
    metadata_storage.delete.assert_called_once_with(metadata)
    transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_track_metadata_missing_is_noop(
    utc_timer: UTCTimer,
    metadata_storage: MetadataStorage,
    object_storage: ObjectStorage,
    outbox_storage: OutboxStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    metadata_storage.get_by_id.return_value = None
    event = create_upload_deleted_event()
    command = make_delete_track_metadata_command(
        metadata_service=create_metadata_service(utc_timer),
        outbox_service=create_outbox_service(utc_timer),
        metadata_storage=metadata_storage,
        object_storage=object_storage,
        outbox_storage=outbox_storage,
        flusher=flusher,
        transaction=transaction,
    )

    await command(event)

    object_storage.delete_object.assert_not_called()
    metadata_storage.delete.assert_not_called()
    flusher.flush.assert_not_called()
    transaction.commit.assert_not_called()
