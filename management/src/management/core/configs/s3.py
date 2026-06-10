"""Module: S3 Configuration."""

from dataclasses import dataclass
from os import environ as env


@dataclass
class S3Config:
    """S3 Configuration object."""

    url: str = env["S3_URL"]
    access_key: str = env["S3_ACCESS_KEY"]
    secret_key: str = env["S3_SECRET_KEY"]
    bucket: str = env["S3_BUCKET"]
    region_name: str = env.get("S3_REGION", "us-east-1")
