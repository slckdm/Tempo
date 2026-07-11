"""Time port."""

from datetime import datetime
from typing import Protocol


class UTCTimer(Protocol):
    """UTC time source."""

    @property
    def now(self) -> datetime:
        """Return current UTC time."""
        ...
