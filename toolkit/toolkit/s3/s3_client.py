from boto3.session import Session
from botocore.config import Config


class S3Client:
    def __init__(
        self, url: str, access_key_id: str, secret_access_key: str, region_name: None | str = None
    ) -> None:
        self.__session = Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name
        )
        self.__client = self.__session.client(
            service_name="s3",
            endpoint_url=url,
            config=Config(signature_version="s3v4"),
        )

    def generate_presigned_url(
        self,
        bucket_name: str,
        object_name: str,
        content_type: None | str = None,
        expiration: int = 3600,
    ) -> str:
        params = {"Bucket": bucket_name, "Key": object_name}
        if content_type is not None:
            params["ContentType"] = content_type
        return self.__client.generate_presigned_url(
            "put_object",
            Params=params,
            ExpiresIn=expiration,
        )
