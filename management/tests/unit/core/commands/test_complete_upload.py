import pytest
from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.object_storage import ObjectStorage
from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.common.services.current_user_service import CurrentUserService
from toolkit.outbox.ports.outbox_storage import OutboxStorage
from toolkit.outbox.service import OutboxService
from toolkit.types.enum import UploadStatus

from app.core.commands.complete_upload import CompleteUpload
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.services.upload_service import UploadService
from tests.unit.core.factories import (
    create_current_user_service,
    create_outbox_service,
    create_upload,
    create_upload_service,
    create_user,
)


def make_complete_upload_command(
    current_user_service: CurrentUserService,
    upload_service: UploadService,
    upload_storage: UploadStorage,
    outbox_service: OutboxService,
    outbox_storage: OutboxStorage,
    object_storage: ObjectStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> CompleteUpload:
    return CompleteUpload(
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
async def test_complete_upload_success(
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
    upload = create_upload(status=UploadStatus.PENDING, created_by=user.id)
    authorized_user_finder.get_by_id.return_value = user
    upload_storage.get_by_id.return_value = upload
    complete_upload_command = make_complete_upload_command(
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
    response = await complete_upload_command(upload.urn)

    upload_storage.get_by_id.assert_called_once_with(upload.id, True)
    object_storage.get_object.assert_called_once_with(str(upload.urn))
    outbox_storage.add.assert_called_once()
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()
