from typing import Iterable

from dishka import Provider

from .s3_provider import S3Provider


def get_outbound_providers() -> Iterable[Provider]:
    return (
        S3Provider(),
    )
