import pytest

from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.contracts.events import MetadataReadyEvent
from tempo_toolkit.contracts.uploads import UploadStatus

from app.core.commands.finish_upload import FinishUpload
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.services.upload_service import UploadService
from tests.unit.core.factories import (
    create_upload,
    create_upload_service,
)


def make_finish_upload_command(
    upload_service: UploadService,
    upload_storage: UploadStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> FinishUpload:
    return FinishUpload(
        upload_service=upload_service,
        upload_storage=upload_storage,
        flusher=flusher,
        transaction=transaction,
    )


@pytest.mark.asyncio
async def test_complete_upload_success(
    upload_storage: UploadStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    upload = create_upload(status=UploadStatus.PROCESSING)
    upload_storage.get_by_id.return_value = upload
    command = make_finish_upload_command(
        upload_service=create_upload_service(),
        upload_storage=upload_storage,
        flusher=flusher,
        transaction=transaction,
    )
    payload = MetadataReadyEvent(upload_id=upload.urn, cover_key="dsf")

    await command(payload)

    upload_storage.get_by_id.assert_called_once_with(upload.urn.id)
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()
