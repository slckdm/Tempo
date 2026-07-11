"""System time integration."""

from datetime import UTC, datetime

from tempo_toolkit.application.time import UTCTimer


class SystemUTCTimer(UTCTimer):
    """System UTC time source."""

    @property
    def now(self) -> datetime:
        """Return current UTC time."""
        return datetime.now(UTC)
