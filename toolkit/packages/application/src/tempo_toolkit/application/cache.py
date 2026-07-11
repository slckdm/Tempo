"""Cache port."""

from typing import Any, Protocol


class Cache(Protocol):
    """Asynchronous key-value cache."""

    async def get(self, key: str) -> Any:
        """Return a cached value."""
        ...

    async def set(self, key: str, value: Any) -> None:
        """Cache a value."""
        ...
