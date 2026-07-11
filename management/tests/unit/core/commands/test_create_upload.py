from typing import Callable
from uuid import UUID

import pytest
from faker import Faker
from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.object_storage import ObjectStorage
from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.common.services.current_user_service import CurrentUserService
from toolkit.outbox.ports.outbox_storage import OutboxStorage
from toolkit.outbox.service import OutboxService

from app.core.commands.create_upload import (
    MAX_UPLOAD_SIZE,
    CreateUpload,
    CreateUploadRequestBody,
)
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.services.upload_service import UploadService
from app.core.models.upload import Upload
from tests.unit.core.factories import (
    create_current_user_service,
    create_outbox_service,
    create_upload_service,
    create_user,
)


def make_create_upload_command(
    current_user_service: CurrentUserService,
    upload_service: UploadService,
    upload_storage: UploadStorage,
    outbox_service: OutboxService,
    outbox_storage: OutboxStorage,
    object_storage: ObjectStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> CreateUpload:
    return CreateUpload(
        current_user_service=current_user_service,
        upload_service=upload_service,
        upload_storage=upload_storage,
        outbox_service=outbox_service,
        outbox_storage=outbox_storage,
        object_storage=object_storage,
        flusher=flusher,
        transaction=transaction,
    )


def __generate_fake_id(uuid: UUID) -> Callable:
    """Generate a fake ID for the upload."""

    async def wrap(upload: Upload) -> None:
        upload.id = uuid

    return wrap


@pytest.mark.asyncio
async def test_create_upload_success(
    faker: Faker,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    utc_timer: UTCTimer,
    upload_storage: UploadStorage,
    outbox_storage: OutboxStorage,
    object_storage: ObjectStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    upload_uuid = Faker().uuid4(cast_to=None)
    user = create_user()
    authorized_user_finder.get_by_id.return_value = user
    object_storage.make_object_upload_url.return_value = "test_url"
    upload_storage.add = __generate_fake_id(upload_uuid)
    create_upload_command = make_create_upload_command(
        current_user_service=create_current_user_service(
            identity_provider, authorized_user_finder
        ),
        upload_service=create_upload_service(),
        outbox_service=create_outbox_service(utc_timer),
        upload_storage=upload_storage,
        outbox_storage=outbox_storage,
        object_storage=object_storage,
        flusher=flusher,
        transaction=transaction,
    )
    request_body = CreateUploadRequestBody.model_validate(
        {
            "filename": faker.file_name("audio"),
            "contentType": faker.mime_type("audio"),
            "size": faker.random_int(min=1, max=MAX_UPLOAD_SIZE),
        }
    )
    response = await create_upload_command(request_body)
    assert response.model_dump() == {
        "upload": f"urn:mng.upload:{upload_uuid}",
        "presigned_url": "test_url",
    }
    object_storage.make_object_upload_url.assert_awaited_once_with(
        f"urn:mng.upload:{upload_uuid}",
        content_type=request_body.content_type,
        content_length=request_body.size,
    )


@pytest.mark.parametrize("size", [0, -1, MAX_UPLOAD_SIZE + 1])
def test_create_upload_request_rejects_invalid_size(size: int) -> None:
    with pytest.raises(ValueError):
        CreateUploadRequestBody(
            filename="test.mp3",
            contentType="audio/mpeg",
            size=size,
        )
