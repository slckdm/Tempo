from datetime import UTC, datetime

from app.core.ports.utc_timer import UTCTimer


class SystemUTCTimer(UTCTimer):
    @property
    def now(self) -> datetime:
        return datetime.now(UTC)
