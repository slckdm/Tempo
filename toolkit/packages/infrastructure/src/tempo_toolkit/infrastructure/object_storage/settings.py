"""S3 settings."""

from pydantic import BaseModel


class S3Settings(BaseModel):
    """S3 connection settings."""

    URL: str
    ACCESS_KEY: str
    SECRET_KEY: str
    BUCKET: str
    REGION_NAME: str = "us-east-1"
