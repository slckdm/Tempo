from botocore.exceptions import ClientError

from toolkit.common.ports.object_storage import ObjectStorage
from toolkit.config.settings import S3Settings
from toolkit.entities.object import Object
from toolkit.s3 import S3Client
from toolkit.service.exceptions import ObjectStorageError


class S3ObjectStorage(ObjectStorage):
    def __init__(self, s3_client: S3Client, s3_settings: S3Settings) -> None:
        self._s3 = s3_client
        self._s3_settings = s3_settings

    async def get_object(self, key: str, **kwargs) -> Object:
        try:
            return await self._s3.get_object(bucket=self._s3_settings.BUCKET, key=key, **kwargs)
        except ClientError as exception:
            raise ObjectStorageError from exception

    async def put_object(self, key: str, body: bytes, **kwargs) -> None:
        try:
            await self._s3.put_object(
                bucket=self._s3_settings.BUCKET, key=key, body=body, **kwargs
            )
        except ClientError as exception:
            raise ObjectStorageError from exception

    async def make_object_upload_url(
        self, key: str, content_type: str, content_length: int
    ) -> str:
        try:
            return await self._s3.generate_presigned_url(
                bucket=self._s3_settings.BUCKET,
                key=key,
                content_type=content_type,
                content_length=content_length,
            )
        except ClientError as exception:
            raise ObjectStorageError from exception

    async def delete_object(self, key: str, **kwargs) -> None:
        try:
            return await self._s3.delete_object(bucket=self._s3_settings.BUCKET, key=key, **kwargs)
        except ClientError as exception:
            raise ObjectStorageError from exception
