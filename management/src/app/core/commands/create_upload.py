from pydantic import BaseModel, Field

from tempo_toolkit.application.auth import CurrentUserService
from tempo_toolkit.application.outbox import OutboxService, OutboxStorage
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.storage import ObjectStorage
from tempo_toolkit.contracts.events import UploadCreatedEvent
from tempo_toolkit.contracts.routing import UPLOAD_CREATED_RK
from tempo_toolkit.contracts.uploads import UploadURN

from app.core.commands.ports.upload_storage import UploadStorage
from app.core.common.enums import AggregateType
from app.core.common.services.upload_service import UploadService
from app.core.models.upload import Upload

MAX_UPLOAD_SIZE = 100 * 1024 * 1024


class CreateUploadResponse(BaseModel):
    """Create upload response body DTO."""

    upload: UploadURN = Field(description="Upload identifier")
    presigned_url: str = Field(
        description="Presigned URL for uploading",
        json_schema_extra={"example": "http://some.url/here/bla-bla-bla"},
    )


class CreateUploadRequestBody(BaseModel):
    """Create upload request body schema."""

    filename: str
    content_type: str = Field(alias="contentType")
    size: int = Field(gt=0, le=MAX_UPLOAD_SIZE, description="File size in bytes")


class CreateUpload:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        upload_service: UploadService,
        upload_storage: UploadStorage,
        outbox_service: OutboxService,
        outbox_storage: OutboxStorage,
        object_storage: ObjectStorage,
        flusher: Flusher,
        transaction: Transaction,
    ) -> None:
        self._current_user_service = current_user_service
        self._upload_service = upload_service
        self._upload_storage = upload_storage
        self._outbox_service = outbox_service
        self._outbox_storage = outbox_storage
        self._object_storage = object_storage
        self._flusher = flusher
        self._transaction = transaction

    async def __call__(
        self,
        body: CreateUploadRequestBody,
    ) -> CreateUploadResponse:
        user = await self._current_user_service.get_current_user(["tempo:etc"])
        upload = await self._upload_service.create_upload(body.filename, body.size, user)
        await self._upload_storage.add(upload)
        url = await self._object_storage.make_object_upload_url(
            str(upload.urn), content_type=body.content_type, content_length=body.size
        )
        await self.__create_event(upload)

        await self._flusher.flush()
        await self._transaction.commit()

        return CreateUploadResponse(upload=upload.urn, presigned_url=url)

    async def __create_event(self, upload: Upload) -> None:
        message = await self._outbox_service.create_message(
            aggregate_type=AggregateType.UPLOAD,
            aggregate_id=str(upload.id),
            event_type=UPLOAD_CREATED_RK,
            payload=UploadCreatedEvent(
                upload_id=upload.urn,
                s3_key=str(upload.urn),
                filename=upload.filename,
                content_type=upload.content_type,
                size=upload.size,
                created_by=upload.created_by,
                created_at=upload.created_at,
                status=upload.status,
            ),
        )
        await self._outbox_storage.add(message)
