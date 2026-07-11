
from tempo_toolkit.application.errors import NotFound
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.contracts.events import MetadataReadyEvent
from tempo_toolkit.contracts.uploads import UploadStatus

from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.services.upload_service import UploadService


class FinishUpload:

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

    async def __call__(self, payload: MetadataReadyEvent) -> None:
        upload = await self._upload_storage.get_by_id(payload.upload_id.id)

        if not upload:
            raise NotFound(data={"upload": str(payload.upload_id)})

        await self._upload_service.transit_status(upload, UploadStatus.COMPLETED)

        await self._flusher.flush()
        await self._transaction.commit()
