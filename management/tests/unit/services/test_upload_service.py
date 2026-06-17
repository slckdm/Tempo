import pytest
from faker import Faker
from .factories import create_upload_service, create_upload, create_user
from app.core.common.services.upload_service import UploadService
from app.core.models import Upload
from app.core.common.enums import UploadStatus

@pytest.mark.asyncio
async def test_create_upload(faker: Faker) -> None:
    upload_service = create_upload_service()
    upload_data = {"filename": "test.mp3", "size": faker.random_number(), "user": create_user()}
    upload = await upload_service.create_upload(**upload_data)

    assert isinstance(upload, Upload)
    assert upload.content_type
    assert upload.filename == upload_data["filename"]
    assert upload.size == upload_data["size"]
    assert str(upload.created_by) == str(upload_data["user"].id)


@pytest.mark.asyncio
async def test_complete_upload() -> None:
    upload_service = create_upload_service()
    upload = create_upload(status=UploadStatus.PENDING)

    await upload_service.complete_upload(upload)

    assert upload.status == UploadStatus.COMPLETED
