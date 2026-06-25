from boto3.exceptions import Boto3Error

from toolkit.entities.object import Object
from toolkit.s3 import S3Client

from app.core.queries.ports.object_storage import ObjectStorage
from app.main.config.settings import S3Settings
from app.outbound.exceptions import StorageError


class S3ObjectStorage(ObjectStorage):

    def __init__(self, s3_client: S3Client, s3_settings: S3Settings) -> None:
        self._s3 = s3_client
        self._s3_settings = s3_settings

    async def get_object(self, key: str, **kwargs) -> Object:
        try:
            return await self._s3.get_object(bucket=self._s3_settings.BUCKET, key=key, **kwargs)
        except Boto3Error as boto3_err:
            raise StorageError from boto3_err

    async def put_object(self, key: str, body: bytes, **kwargs) -> None:
        try:
            await self._s3.put_object(
                bucket=self._s3_settings.BUCKET, key=key, body=body, **kwargs
            )
        except Boto3Error as boto3_err:
            raise StorageError from boto3_err

    async def stream(self, key: str, range_header: str | None) -> Object:
        kwargs = {}
        if range_header:
            kwargs["Range"] = range_header
        return await self.get_object(key=key, **kwargs)
