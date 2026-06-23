import asyncio

from boto3.session import Session
from botocore.config import Config
from botocore.exceptions import ClientError

from toolkit.entities.object import Object


class NoSuchKeyException(Exception):
    """Exception indicating that no object found."""


class S3Client:
    """S3 API client."""

    def __init__(
        self, url: str, access_key_id: str, secret_access_key: str, region_name: None | str = None
    ) -> None:
        """Initialize S3 API client."""
        self._session = Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
        )
        self._client = self._session.client(
            service_name="s3",
            endpoint_url=url,
            config=Config(signature_version="s3v4"),
        )

    async def get_object(self, bucket: str, key: str, **kwargs) -> Object:
        """Get existing object."""
        try:
            response_data = await asyncio.to_thread(
                self._client.get_object, Bucket=bucket, Key=key, **kwargs
            )
            return Object.model_validate(response_data)

        except Exception as exc:
            if "NoSuchKey" in str(exc):
                raise NoSuchKeyException from exc
            else:
                raise exc

    def generate_presigned_url(
        self,
        bucket: str,
        key: str,
        content_type: None | str = None,
        expiration: int = 3600,
    ) -> str:
        """Generate presigned url for creating a new object."""
        params = {"Bucket": bucket, "Key": key}
        if content_type is not None:
            params["ContentType"] = content_type
        return self._client.generate_presigned_url(
            "put_object",
            Params=params,
            ExpiresIn=expiration,
        )

    async def put_object(
        self, bucket: str, key: str, body: bytes, **kwargs
    ) -> None:
        try:
            await asyncio.to_thread(
                self._client.put_object,
                Bucket=bucket,
                Key=key,
                Body=body,
                **kwargs,
            )
        except ClientError as client_err:
            raise client_err
