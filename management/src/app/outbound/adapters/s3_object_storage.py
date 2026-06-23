from toolkit.entities.object import Object
from toolkit.s3 import S3Client

from app.core.ports.object_storage import ObjectStorage
from app.main.config.settings import S3Settings


class S3ObjectStorage(ObjectStorage):

    def __init__(self, s3_client: S3Client, s3_settings: S3Settings) -> None:
        self._s3 = s3_client
        self._s3_settings = s3_settings

    async def get_object(self, key: str) -> Object:
        return await self._s3.get_object(bucket=self._s3_settings.BUCKET, key=key)

    async def put_object(self, key: str, body: bytes, **kwargs) -> None:
        await self._s3.put_object(
            bucket=self._s3_settings.BUCKET, key=key, body=body, **kwargs
        )
