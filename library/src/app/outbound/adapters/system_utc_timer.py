from datetime import UTC, datetime

from app.core.common.ports.utc_timer import UTCTimer


class SystemUTCTimer(UTCTimer):
    @property
    def now(self) -> datetime:
        return datetime.now(UTC)
