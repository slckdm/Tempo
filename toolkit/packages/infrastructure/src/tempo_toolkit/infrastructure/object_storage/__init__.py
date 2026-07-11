"""S3 object-storage integration."""

from .adapter import S3ObjectStorage
from .provider import S3Provider
from .s3 import S3Client
from .settings import S3Settings

__all__ = ["S3Client", "S3ObjectStorage", "S3Provider", "S3Settings"]
