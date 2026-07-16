import io

import pytest

from tempo_toolkit.application.auth import (
    AuthorizedUserFinder,
    CurrentUserService,
    IdentityProvider,
)
from tempo_toolkit.application.outbox import OutboxService, OutboxStorage
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage, StoredObject
from tempo_toolkit.application.time import UTCTimer
from tempo_toolkit.contracts.uploads import UploadStatus

from app.core.commands.complete_upload import CompleteUpload
from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.ports.metadata_proxy import MetadataProxy
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
    object_storage: ObjectStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> CompleteUpload:
    return CompleteUpload(
        current_user_service=current_user_service,
        upload_service=upload_service,
        upload_storage=upload_storage,
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
    stored_object = StoredObject(
        body=io.BytesIO(b"audio"),
        content_length=5,
        content_type="audio/mpeg",
    )

    authorized_user_finder.get_by_id.return_value = user
    upload_storage.get_by_id.return_value = upload
    object_storage.get_object.return_value = stored_object

    complete_upload_command = make_complete_upload_command(
        current_user_service=create_current_user_service(
            identity_provider, authorized_user_finder
        ),
        upload_service=create_upload_service(create_outbox_service(utc_timer), outbox_storage),
        upload_storage=upload_storage,
        object_storage=object_storage,
        flusher=flusher,
        transaction=transaction,
    )
    await complete_upload_command(upload.urn)

    upload_storage.get_by_id.assert_called_once_with(upload.id, True)
    object_storage.get_object.assert_called_once_with(str(upload.urn))
    assert stored_object.body.closed
    outbox_storage.add.assert_called_once()
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()
