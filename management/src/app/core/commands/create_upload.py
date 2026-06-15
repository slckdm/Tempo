from toolkit.s3 import S3Client
from toolkit.service.response import JSendSuccessfulResponse

from app.core.ports.flusher import Flusher
from app.core.ports.transaction import Transaction
from app.core.ports.upload_storage import UploadStorage
from app.main.config.settings import S3Settings
from app.schemas.dto import UploadDTO
from app.schemas.request import CreateUploadRequestBody
from app.schemas.response import CreateUploadResponseBody
from app.services.current_user_service import CurrentUserService
from app.services.upload_service import UploadService


class CreateUpload:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        upload_service: UploadService,
        s3: S3Client,
        s3_config: S3Settings,
        flusher: Flusher,
        transaction: Transaction,
        upload_storage: UploadStorage,
    ) -> None:
        self._current_user_service = current_user_service
        self._upload_service = upload_service
        self._s3 = s3
        self._s3_config = s3_config
        self._flusher = flusher
        self._transaction = transaction
        self._upload_storage = upload_storage

    async def execute(
        self,
        body: CreateUploadRequestBody,
    ) -> JSendSuccessfulResponse[CreateUploadResponseBody]:
        user = await self._current_user_service.get_current_user()
        presigned_url = self._s3.generate_presigned_url(
            self._s3_config.BUCKET, body.filename, content_type=body.content_type
        )
        upload = await self._upload_service.create_upload(
            body.filename, body.content_type, body.size, user
        )
        await self._upload_storage.add(upload)
        await self._flusher.flush([upload])
        await self._transaction.commit()

        return JSendSuccessfulResponse(
            data=CreateUploadResponseBody(
                upload=UploadDTO(urn=upload.urn),
                presigned_url=presigned_url,
            )
        )
