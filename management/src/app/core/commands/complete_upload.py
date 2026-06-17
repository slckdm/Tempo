from toolkit.s3 import S3Client
from toolkit.service.response import JSendSuccessfulResponse

from app.core.common.enums.aggregate_type import AggregateType
from app.core.common.enums.event_type import EventType
from app.core.common.services import CurrentUserService, OutboxService, UploadService
from app.core.common.types_ import UploadURNType
from app.core.ports.outbox_storage import OutboxStorage
from app.core.ports.transaction import Transaction
from app.core.ports.upload_storage import UploadStorage
from app.core.schemas.response import CompleteUploadResponseBody
from app.main.config.settings import S3Settings


class CompleteUpload:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        upload_service: UploadService,
        upload_storage: UploadStorage,
        outbox_service: OutboxService,
        outbox_storage: OutboxStorage,
        s3: S3Client,
        s3_config: S3Settings,
        transaction: Transaction,
    ) -> None:
        self._current_user_service = current_user_service
        self._upload_service = upload_service
        self._upload_storage = upload_storage
        self._outbox_service = outbox_service
        self._outbox_storage = outbox_storage
        self._s3 = s3
        self._s3_config = s3_config
        self._transaction = transaction

    async def execute(
        self, upload_id: UploadURNType
    ) -> JSendSuccessfulResponse[CompleteUploadResponseBody]:
        await self._current_user_service.get_current_user()
        upload = await self._upload_storage.get_by_id(upload_id.id, for_update=True)
        self._s3.get_object(bucket_name=self._s3_config.BUCKET, key=str(upload.urn))
        await self._upload_service.complete_upload(upload)
        message = await self._outbox_service.create_message(
            aggregate_type=AggregateType.UPLOAD,
            aggregate_id=str(upload.id),
            event_type=EventType.UPLOAD_COMPLETED,
            payload={},
        )
        await self._outbox_storage.add(message)
        await self._transaction.commit()

        return JSendSuccessfulResponse(data=CompleteUploadResponseBody())
