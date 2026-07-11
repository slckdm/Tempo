"""S3 object-storage adapter."""

from botocore.exceptions import ClientError

from tempo_toolkit.application.errors import ObjectStorageError
from tempo_toolkit.application.storage import ObjectStorage, StoredObject

from .s3 import S3Client
from .settings import S3Settings


class S3ObjectStorage(ObjectStorage):
    """Application object storage backed by S3."""

    def __init__(self, s3_client: S3Client, s3_settings: S3Settings) -> None:
        """Initialize the adapter with an S3 client and settings."""
        self._s3 = s3_client
        self._s3_settings = s3_settings

    async def get_object(self, key: str, **kwargs: object) -> StoredObject:
        """Get an object from the configured bucket."""
        try:
            return await self._s3.get_object(bucket=self._s3_settings.BUCKET, key=key, **kwargs)
        except ClientError as exception:
            raise ObjectStorageError from exception

    async def put_object(self, key: str, body: bytes, **kwargs: object) -> None:
        """Store an object in the configured bucket."""
        try:
            await self._s3.put_object(
                bucket=self._s3_settings.BUCKET, key=key, body=body, **kwargs
            )
        except ClientError as exception:
            raise ObjectStorageError from exception

    async def make_object_upload_url(
        self, key: str, content_type: str, content_length: int
    ) -> str:
        """Generate a presigned upload URL."""
        try:
            return await self._s3.generate_presigned_url(
                bucket=self._s3_settings.BUCKET,
                key=key,
                content_type=content_type,
                content_length=content_length,
            )
        except ClientError as exception:
            raise ObjectStorageError from exception

    async def delete_object(self, key: str, **kwargs: object) -> None:
        """Delete an object from the configured bucket."""
        try:
            await self._s3.delete_object(bucket=self._s3_settings.BUCKET, key=key, **kwargs)
        except ClientError as exception:
            raise ObjectStorageError from exception
