import pytest

from tempo_toolkit.application.outbox import OutboxService, OutboxStorage
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.application.time import UTCTimer

from app.core.commands.ports.metadata_parser import MetadataParser
from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.commands.process_track_metadata import ProcessTrackMetadata
from app.core.common.exceptions import MetadataAlreadyProcessed
from app.core.common.services.metadata_service import MetadataService
from tests.unit.core.factories import (
    create_cover,
    create_metadata,
    create_metadata_service,
    create_object,
    create_outbox_service,
    create_track_metadata,
    create_upload_completed_event,
)


def make_process_track_metadata_command(
    metadata_service: MetadataService,
    metadata_storage: MetadataStorage,
    metadata_parser: MetadataParser,
    object_storage: ObjectStorage,
    outbox_storage: OutboxStorage,
    outbox_service: OutboxService,
    transaction: Transaction,
    flusher: Flusher,
) -> ProcessTrackMetadata:
    return ProcessTrackMetadata(
        metadata_service=metadata_service,
        metadata_storage=metadata_storage,
        metadata_parser=metadata_parser,
        object_storage=object_storage,
        outbox_storage=outbox_storage,
        outbox_service=outbox_service,
        transaction=transaction,
        flusher=flusher,
    )


@pytest.mark.asyncio
async def test_process_track_metadata_success(
    utc_timer: UTCTimer,
    metadata_storage: MetadataStorage,
    metadata_parser: MetadataParser,
    object_storage: ObjectStorage,
    outbox_storage: OutboxStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    event = create_upload_completed_event()
    metadata_storage.get_by_id.return_value = None
    object_storage.get_object.return_value = create_object()
    metadata_parser.read.return_value = create_metadata(cover=None)
    command = make_process_track_metadata_command(
        metadata_service=create_metadata_service(utc_timer),
        outbox_service=create_outbox_service(utc_timer),
        metadata_storage=metadata_storage,
        metadata_parser=metadata_parser,
        object_storage=object_storage,
        outbox_storage=outbox_storage,
        flusher=flusher,
        transaction=transaction,
    )

    await command(event)

    metadata_storage.get_by_id.assert_called_once_with(event.upload_id.id)
    object_storage.get_object.assert_called_once_with(event.s3_key)
    object_storage.put_object.assert_not_called()
    added = metadata_storage.add.call_args.args[0]
    assert added.cover_key is None
    outbox_storage.add.assert_called_once()
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_process_track_metadata_stores_cover(
    utc_timer: UTCTimer,
    metadata_storage: MetadataStorage,
    metadata_parser: MetadataParser,
    object_storage: ObjectStorage,
    outbox_storage: OutboxStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    event = create_upload_completed_event()
    cover = create_cover(data=b"cover-bytes", mime_type="image/jpeg")
    metadata_storage.get_by_id.return_value = None
    object_storage.get_object.return_value = create_object()
    metadata_parser.read.return_value = create_metadata(cover=cover)
    command = make_process_track_metadata_command(
        metadata_service=create_metadata_service(utc_timer),
        outbox_service=create_outbox_service(utc_timer),
        metadata_storage=metadata_storage,
        metadata_parser=metadata_parser,
        object_storage=object_storage,
        outbox_storage=outbox_storage,
        flusher=flusher,
        transaction=transaction,
    )

    await command(event)

    expected_cover_key = f"covers/{event.s3_key}"
    object_storage.put_object.assert_called_once_with(
        expected_cover_key, body=cover.data, ContentType="image/jpeg"
    )
    added = metadata_storage.add.call_args.args[0]
    assert added.cover_key == expected_cover_key
    transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_process_track_metadata_already_processed(
    utc_timer: UTCTimer,
    metadata_storage: MetadataStorage,
    metadata_parser: MetadataParser,
    object_storage: ObjectStorage,
    outbox_storage: OutboxStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    event = create_upload_completed_event()
    metadata_storage.get_by_id.return_value = create_track_metadata()
    command = make_process_track_metadata_command(
        metadata_service=create_metadata_service(utc_timer),
        outbox_service=create_outbox_service(utc_timer),
        metadata_storage=metadata_storage,
        metadata_parser=metadata_parser,
        object_storage=object_storage,
        outbox_storage=outbox_storage,
        flusher=flusher,
        transaction=transaction,
    )

    with pytest.raises(MetadataAlreadyProcessed):
        await command(event)

    object_storage.get_object.assert_not_called()
    metadata_storage.add.assert_not_called()
    outbox_storage.add.assert_not_called()
    transaction.commit.assert_not_called()
