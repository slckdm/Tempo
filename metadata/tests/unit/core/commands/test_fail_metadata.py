import pytest

from toolkit.messaging.routing import METADATA_FAILED_RK
from toolkit.types.enum import UploadStatus

from app.core.commands.fail_metadata import FailMetadata
from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.metadata_storage import MetadataStorage
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.common.exceptions import TagParseError
from app.core.common.ports.utc_timer import UTCTimer
from app.core.common.services.metadata_service import MetadataService
from app.core.common.services.outbox_service import OutboxService
from tests.unit.core.factories import (
    create_metadata_service,
    create_outbox_service,
    create_upload_completed_event,
)


def make_fail_metadata_command(
    flusher: Flusher,
    transaction: Transaction,
    outbox_storage: OutboxStorage,
    outbox_service: OutboxService,
    metadata_storage: MetadataStorage,
    metadata_service: MetadataService,
) -> FailMetadata:
    return FailMetadata(
        flusher=flusher,
        transaction=transaction,
        outbox_storage=outbox_storage,
        outbox_service=outbox_service,
        metadata_storage=metadata_storage,
        metadata_service=metadata_service,
    )


@pytest.mark.asyncio
async def test_fail_metadata_success(
    utc_timer: UTCTimer,
    metadata_storage: MetadataStorage,
    outbox_storage: OutboxStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    event = create_upload_completed_event()
    exception = TagParseError()
    command = make_fail_metadata_command(
        metadata_service=create_metadata_service(utc_timer),
        outbox_service=create_outbox_service(utc_timer),
        metadata_storage=metadata_storage,
        outbox_storage=outbox_storage,
        flusher=flusher,
        transaction=transaction,
    )

    await command(event, exception)

    transaction.rollback.assert_called_once()
    stored = metadata_storage.add.call_args.args[0]
    assert stored.processing_status == UploadStatus.FAILED
    assert stored.error == str(exception)
    message = outbox_storage.add.call_args.args[0]
    assert message.event_type == str(METADATA_FAILED_RK)
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()
