from tempo_toolkit.application.auth import CurrentUserService
from tempo_toolkit.application.errors import Forbidden, NotFound
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.contracts.uploads import UploadURN

from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.services.upload_service import UploadService


class CompleteUpload:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        upload_service: UploadService,
        upload_storage: UploadStorage,
        object_storage: ObjectStorage,
        transaction: Transaction,
        flusher: Flusher,
    ) -> None:
        self._current_user_service = current_user_service
        self._upload_service = upload_service
        self._upload_storage = upload_storage
        self._object_storage = object_storage
        self._transaction = transaction
        self._flusher = flusher

    async def __call__(self, upload_id: UploadURN) -> None:
        user = await self._current_user_service.get_current_user(["tempo:etc"])
        upload = await self._upload_storage.get_by_id(upload_id.id, for_update=True)

        if not upload:
            raise NotFound(data={"upload": upload_id})
        if upload.created_by != user.id:
            raise Forbidden()

        object = await self._object_storage.get_object(str(upload.urn))
        object.body.close()

        await self._upload_service.complete_upload(upload)
        await self._upload_service.make_upload_completed_event(upload)

        await self._flusher.flush()
        await self._transaction.commit()
