import pytest
from faker import Faker

from app.core.commands.create_upload import CreateUpload, CreateUploadRequestBody
from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.object_storage import ObjectStorage
from app.core.commands.ports.outbox_storage import OutboxStorage
from app.core.commands.ports.transaction import Transaction
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.ports.utc_timer import UTCTimer
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.outbox_service import OutboxService
from app.core.common.services.upload_service import UploadService
from tests.unit.core.factories import (
    create_current_user_service,
    create_outbox_service,
    create_upload_service,
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
    object_storage.make_object_upload_url.return_value = "test_url"
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
            "size": faker.random_number(),
        }
    )
    response = await create_upload_command(request_body)
    assert response.model_dump() == {
        "upload": "urn:mng.upload:None",
        "presigned_url": "test_url",
    }
