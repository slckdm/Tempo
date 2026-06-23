from typing import Iterable

from dishka import Provider

from app.main.ioc.core import CoreProvider


def get_providers() -> Iterable[Provider]:
    return (
        CoreProvider(),
    )
