"""Module: S3 Client."""

from toolkit.s3 import S3Client

from management.core.configs import S3Config

s3_client = S3Client(
    # region_name=S3Config.region_name,
    url=S3Config.url,
    access_key_id=S3Config.access_key,
    secret_access_key=S3Config.secret_key,
)
