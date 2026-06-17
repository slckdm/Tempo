from boto3.session import Session
from botocore.config import Config
from mypy_boto3_s3.type_defs import GetObjectOutputTypeDef


class NoSuchKeyException(Exception):
    """Exception indicating that no object found."""


class S3Client:
    """S3 API client."""

    def __init__(
        self, url: str, access_key_id: str, secret_access_key: str, region_name: None | str = None
    ) -> None:
        """Initialize S3 API client."""
        self.__session = Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
        )
        self.__client = self.__session.client(
            service_name="s3",
            endpoint_url=url,
            config=Config(signature_version="s3v4"),
        )

    def get_object(self, bucket_name: str, key: str, **kwargs) -> GetObjectOutputTypeDef | None:
        """Get existing object."""
        try:
            return self.__client.get_object(
                Bucket=bucket_name,
                Key=key,
                **kwargs
            )
        except Exception as exc:
            if "NoSuchKey" in str(exc):
                raise NoSuchKeyException from exc
            else:
                raise exc

    def generate_presigned_url(
        self,
        bucket_name: str,
        object_name: str,
        content_type: None | str = None,
        expiration: int = 3600,
    ) -> str:
        """Generate presigned url for creating a new object."""
        params = {"Bucket": bucket_name, "Key": object_name}
        if content_type is not None:
            params["ContentType"] = content_type
        return self.__client.generate_presigned_url(
            "put_object",
            Params=params,
            ExpiresIn=expiration,
        )
