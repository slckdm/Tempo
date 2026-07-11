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
from toolkit.service.exceptions import Conflict, Forbidden, NotFound
from toolkit.types.enum import UploadStatus
from toolkit.types.urn import UploadURNType

from app.core.commands.delete_upload import DeleteUpload
from app.core.commands.ports.upload_storage import UploadStorage
from tests.unit.core.factories import (
    create_current_user_service,
    create_outbox_service,
    create_upload,
    create_user,
)


def make_delete_upload_command(
    upload_storage: UploadStorage,
    outbox_service: OutboxService,
    outbox_storage: OutboxStorage,
    object_storage: ObjectStorage,
    flusher: Flusher,
    current_user_service: CurrentUserService,
    transaction: Transaction,
) -> DeleteUpload:
    return DeleteUpload(
        current_user_service=current_user_service,
        upload_storage=upload_storage,
        outbox_storage=outbox_storage,
        object_storage=object_storage,
        outbox_service=outbox_service,
        flusher=flusher,
        transaction=transaction,
    )


@pytest.mark.asyncio
async def test_delete_upload_success(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    utc_timer: UTCTimer,
    upload_storage: UploadStorage,
    outbox_storage: OutboxStorage,
    object_storage: ObjectStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    upload = create_upload(status=UploadStatus.COMPLETED, created_by=user.id)
    upload_storage.get_by_id.return_value = upload
    authorized_user_finder.get_by_id.return_value = user

    delete_upload_command = make_delete_upload_command(
        current_user_service=create_current_user_service(
            identity_provider, authorized_user_finder
        ),
        outbox_service=create_outbox_service(utc_timer),
        upload_storage=upload_storage,
        outbox_storage=outbox_storage,
        object_storage=object_storage,
        flusher=flusher,
        transaction=transaction,
    )
    await delete_upload_command(upload.urn)


@pytest.mark.asyncio
async def test_delete_upload_forbidden(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    utc_timer: UTCTimer,
    upload_storage: UploadStorage,
    outbox_storage: OutboxStorage,
    object_storage: ObjectStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    upload = create_upload(status=UploadStatus.COMPLETED)
    upload_storage.get_by_id.return_value = upload
    delete_upload_command = make_delete_upload_command(
        current_user_service=create_current_user_service(
            identity_provider, authorized_user_finder
        ),
        outbox_service=create_outbox_service(utc_timer),
        upload_storage=upload_storage,
        outbox_storage=outbox_storage,
        object_storage=object_storage,
        flusher=flusher,
        transaction=transaction,
    )
    with pytest.raises(Forbidden):
        await delete_upload_command(upload.urn)


@pytest.mark.asyncio
async def test_delete_upload_conflict(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    utc_timer: UTCTimer,
    upload_storage: UploadStorage,
    outbox_storage: OutboxStorage,
    object_storage: ObjectStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    upload = create_upload(status=UploadStatus.PENDING)
    upload_storage.get_by_id.return_value = upload

    delete_upload_command = make_delete_upload_command(
        current_user_service=create_current_user_service(
            identity_provider, authorized_user_finder
        ),
        outbox_service=create_outbox_service(utc_timer),
        upload_storage=upload_storage,
        outbox_storage=outbox_storage,
        object_storage=object_storage,
        flusher=flusher,
        transaction=transaction,
    )
    with pytest.raises(Conflict):
        await delete_upload_command(upload.urn)


@pytest.mark.asyncio
async def test_delete_upload_not_found(
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
    upload_storage.get_by_id.return_value = None

    delete_upload_command = make_delete_upload_command(
        current_user_service=create_current_user_service(
            identity_provider, authorized_user_finder
        ),
        outbox_service=create_outbox_service(utc_timer),
        upload_storage=upload_storage,
        outbox_storage=outbox_storage,
        object_storage=object_storage,
        flusher=flusher,
        transaction=transaction,
    )
    with pytest.raises(NotFound):
        await delete_upload_command(UploadURNType(faker.uuid4(cast_to=None)))
