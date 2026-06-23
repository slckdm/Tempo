
from toolkit.messaging.contracts import MetadataFailedEvent
from toolkit.service.exceptions import NotFoundException
from toolkit.types.enum import UploadStatus

from app.core.common.services.upload_service import UploadService
from app.core.ports.flusher import Flusher
from app.core.ports.transaction import Transaction
from app.core.ports.upload_storage import UploadStorage


class FailUpload:

    def __init__(
        self,
        upload_service: UploadService,
        upload_storage: UploadStorage,
        transaction: Transaction,
        flusher: Flusher,
    ) -> None:
        self._upload_service = upload_service
        self._upload_storage = upload_storage
        self._transaction = transaction
        self._flusher = flusher

    async def __call__(self, payload: MetadataFailedEvent) -> None:
        upload = await self._upload_storage.get_by_id(payload.upload_id.id)

        if not upload:
            raise NotFoundException(data={"upload": str(payload.upload_id)})

        await self._upload_service.transit_status(upload, UploadStatus.FAILED)
        await self._flusher.flush()
        await self._transaction.commit()
