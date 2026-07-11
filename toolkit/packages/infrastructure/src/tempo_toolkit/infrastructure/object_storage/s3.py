"""S3 client."""

import asyncio

from boto3.session import Session
from botocore.config import Config

from tempo_toolkit.application.storage import StoredObject


class S3Client:
    """Asynchronous facade over the blocking boto3 S3 client."""

    def __init__(
        self, url: str, access_key_id: str, secret_access_key: str, region_name: str | None = None
    ) -> None:
        """Initialize the client with S3 connection settings."""
        session = Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
        )
        self._client = session.client(
            service_name="s3",
            endpoint_url=url,
            config=Config(signature_version="s3v4"),
        )

    async def get_object(self, bucket: str, key: str, **kwargs: object) -> StoredObject:
        """Get an object."""
        response = await asyncio.to_thread(
            self._client.get_object, Bucket=bucket, Key=key, **kwargs
        )
        return StoredObject(
            body=response["Body"],
            content_range=response.get("ContentRange"),
            content_length=response["ContentLength"],
            content_type=response["ContentType"],
        )

    async def generate_presigned_url(
        self,
        bucket: str,
        key: str,
        content_type: str | None = None,
        content_length: int | None = None,
        expiration: int = 3600,
    ) -> str:
        """Generate a presigned object-upload URL."""
        params: dict[str, str | int] = {"Bucket": bucket, "Key": key}
        if content_type is not None:
            params["ContentType"] = content_type
        if content_length is not None:
            params["ContentLength"] = content_length
        return await asyncio.to_thread(
            self._client.generate_presigned_url,
            "put_object",
            Params=params,
            ExpiresIn=expiration,
        )

    async def put_object(self, bucket: str, key: str, body: bytes, **kwargs: object) -> None:
        """Store an object."""
        await asyncio.to_thread(
            self._client.put_object, Bucket=bucket, Key=key, Body=body, **kwargs
        )

    async def delete_object(self, bucket: str, key: str, **kwargs: object) -> None:
        """Delete an object."""
        await asyncio.to_thread(self._client.delete_object, Bucket=bucket, Key=key, **kwargs)
