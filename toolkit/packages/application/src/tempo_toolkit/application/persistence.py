"""Persistence ports."""

from collections.abc import Sequence
from typing import Any, Protocol


class Flusher(Protocol):
    """Flush pending persistence changes."""

    async def flush(self, objects: Sequence[Any] | None = None) -> None:
        """Flush pending changes."""
        ...


class Transaction(Protocol):
    """Database transaction boundary."""

    async def commit(self) -> None:
        """Commit the transaction."""
        ...

    async def rollback(self) -> None:
        """Roll back the transaction."""
        ...
