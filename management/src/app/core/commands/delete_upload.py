from tempo_toolkit.application.auth import CurrentUserService
from tempo_toolkit.application.errors import Conflict, Forbidden, NotFound
from tempo_toolkit.application.outbox import OutboxService, OutboxStorage
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.contracts.events import UploadDeletedEvent
from tempo_toolkit.contracts.routing import UPLOAD_DELETED_RK
from tempo_toolkit.contracts.uploads import UploadStatus, UploadURN

from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.enums.aggregate_type import AggregateType
from app.core.models.upload import Upload


class DeleteUpload:
    def __init__(
        self,
        object_storage: ObjectStorage,
        outbox_storage: OutboxStorage,
        upload_storage: UploadStorage,
        current_user_service: CurrentUserService,
        outbox_service: OutboxService,
        flusher: Flusher,
        transaction: Transaction,
    ):
        self._flusher = flusher
        self._object_storage = object_storage
        self._outbox_storage = outbox_storage
        self._transaction = transaction
        self._upload_storage = upload_storage
        self._current_user_service = current_user_service
        self._outbox_service = outbox_service

    async def __call__(self, upload_id: UploadURN) -> None:
        user = await self._current_user_service.get_current_user(["tempo:etc"])
        upload = await self._upload_storage.get_by_id(upload_id.id, for_update=True)

        if not upload:
            raise NotFound
        elif upload.status not in (UploadStatus.COMPLETED, UploadStatus.FAILED):
            raise Conflict
        elif user.id != upload.created_by:
            raise Forbidden

        await self.__create_event(upload)
        await self._upload_storage.delete(upload)
        await self._object_storage.delete_object(str(upload_id))

        await self._flusher.flush()
        await self._transaction.commit()

    async def __create_event(self, upload: Upload) -> None:
        message = await self._outbox_service.create_message(
            AggregateType.UPLOAD,
            str(upload.id),
            UPLOAD_DELETED_RK,
            UploadDeletedEvent(
                upload_id=upload.urn,
                s3_key=str(upload.urn),
            ),
        )
        await self._outbox_storage.add(message)
