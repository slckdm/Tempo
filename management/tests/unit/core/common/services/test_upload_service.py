import pytest
from faker import Faker

from tempo_toolkit.application.outbox.ports import OutboxStorage
from tempo_toolkit.application.time import UTCTimer
from tempo_toolkit.contracts.uploads import UploadStatus

from app.core.common.exceptions import StatusUpdateFlowError
from app.core.common.ports.metadata_proxy import MetadataProxy
from app.core.models.upload import Upload
from tests.unit.core.factories import (
    create_outbox_service,
    create_upload,
    create_upload_service,
    create_user,
)


@pytest.mark.asyncio
async def test_create_upload(
    faker: Faker, utc_timer: UTCTimer, outbox_storage: OutboxStorage
) -> None:
    outbox_service = create_outbox_service(utc_timer)
    upload_service = create_upload_service(outbox_service, outbox_storage)
    upload_data = {"filename": "test.mp3", "size": faker.random_number(), "user": create_user()}
    upload = await upload_service.create_upload(**upload_data)

    assert isinstance(upload, Upload)
    assert upload.content_type
    assert upload.filename == upload_data["filename"]
    assert upload.size == upload_data["size"]
    assert str(upload.created_by) == str(upload_data["user"].id)


@pytest.mark.asyncio
async def test_complete_upload_success(utc_timer: UTCTimer, outbox_storage: OutboxStorage) -> None:
    outbox_service = create_outbox_service(utc_timer)
    upload_service = create_upload_service(outbox_service, outbox_storage)
    upload = create_upload(status=UploadStatus.PENDING)

    await upload_service.transit_status(upload, UploadStatus.PROCESSING)

    assert upload.status == UploadStatus.PROCESSING


@pytest.mark.asyncio
async def test_complete_upload_fail_flow(
    utc_timer: UTCTimer, outbox_storage: OutboxStorage
) -> None:
    outbox_service = create_outbox_service(utc_timer)
    upload_service = create_upload_service(outbox_service, outbox_storage)
    upload = create_upload(status=UploadStatus.PENDING)

    with pytest.raises(StatusUpdateFlowError):
        await upload_service.transit_status(upload, UploadStatus.COMPLETED)

    assert upload.status == UploadStatus.PENDING
