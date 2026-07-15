from tempo_toolkit.application.auth import CurrentUserService
from tempo_toolkit.application.errors import Conflict, Forbidden, NotFound
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.contracts.uploads import UploadStatus, UploadURN

from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.services.upload_service import UploadService


class DeleteUpload:
    def __init__(
        self,
        object_storage: ObjectStorage,
        upload_storage: UploadStorage,
        upload_service: UploadService,
        current_user_service: CurrentUserService,
        flusher: Flusher,
        transaction: Transaction,
    ):
        self._flusher = flusher
        self._object_storage = object_storage
        self._transaction = transaction
        self._upload_storage = upload_storage
        self._upload_service = upload_service
        self._current_user_service = current_user_service

    async def __call__(self, upload_id: UploadURN) -> None:
        user = await self._current_user_service.get_current_user(["tempo:etc"])
        upload = await self._upload_storage.get_by_id(upload_id.id, for_update=True)

        if not upload:
            raise NotFound
        elif upload.status not in (UploadStatus.COMPLETED, UploadStatus.FAILED):
            raise Conflict
        elif user.id != upload.created_by:
            raise Forbidden

        await self._upload_service.make_upload_deleted_event(upload)
        await self._upload_storage.delete(upload)
        await self._object_storage.delete_object(str(upload_id))

        await self._flusher.flush()
        await self._transaction.commit()
