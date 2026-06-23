from abc import abstractmethod
from datetime import datetime
from typing import Protocol


class UTCTimer(Protocol):

    @property
    @abstractmethod
    def now(self) -> datetime: ...
