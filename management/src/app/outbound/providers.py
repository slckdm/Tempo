from typing import Iterable

from dishka import Provider

from .postgres_provider import PostgresProvider
from .s3_provider import S3Provider


def get_outbound_providers() -> Iterable[Provider]:
    return (
        PostgresProvider(),
        S3Provider(),
    )
