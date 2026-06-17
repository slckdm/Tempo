from toolkit.s3 import S3Client
from toolkit.service.response import JSendSuccessfulResponse

from app.core.common.enums import AggregateType, EventType
from app.core.common.services import CurrentUserService, OutboxService, UploadService
from app.core.ports.flusher import Flusher
from app.core.ports.outbox_storage import OutboxStorage
from app.core.ports.transaction import Transaction
from app.core.ports.upload_storage import UploadStorage
from app.core.schemas.dto import UploadDTO
from app.core.schemas.request import CreateUploadRequestBody
from app.core.schemas.response import CreateUploadResponseBody
from app.main.config.settings import S3Settings


class CreateUpload:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        upload_service: UploadService,
        upload_storage: UploadStorage,
        outbox_service: OutboxService,
        outbox_storage: OutboxStorage,
        s3: S3Client,
        s3_config: S3Settings,
        flusher: Flusher,
        transaction: Transaction,
    ) -> None:
        self._current_user_service = current_user_service
        self._upload_service = upload_service
        self._upload_storage = upload_storage
        self._outbox_service = outbox_service
        self._outbox_storage = outbox_storage
        self._s3 = s3
        self._s3_config = s3_config
        self._flusher = flusher
        self._transaction = transaction

    async def execute(
        self,
        body: CreateUploadRequestBody,
    ) -> JSendSuccessfulResponse[CreateUploadResponseBody]:
        user = await self._current_user_service.get_current_user()
        upload = await self._upload_service.create_upload(body.filename, body.size, user)
        await self._upload_storage.add(upload)
        await self._flusher.flush([upload])
        presigned_url = self._s3.generate_presigned_url(
            self._s3_config.BUCKET, str(upload.urn), content_type=body.content_type
        )
        message = await self._outbox_service.create_message(
            aggregate_type=AggregateType.UPLOAD,
            aggregate_id=str(upload.id),
            event_type=EventType.UPLOAD_CREATED,
            payload={},
        )
        await self._outbox_storage.add(message)

        await self._transaction.commit()

        return JSendSuccessfulResponse(
            data=CreateUploadResponseBody(
                upload=UploadDTO(urn=upload.urn),
                presigned_url=presigned_url,
            )
        )
