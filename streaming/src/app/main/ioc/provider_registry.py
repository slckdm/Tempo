from typing import Sequence

from dishka import Provider

from .core import CoreProvider


def get_providers() -> Sequence[Provider]:
    return (CoreProvider(),)
