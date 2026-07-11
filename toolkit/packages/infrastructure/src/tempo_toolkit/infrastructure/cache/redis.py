"""Redis cache adapter."""

from typing import Any

from redis.asyncio.client import Redis

from tempo_toolkit.application.cache import Cache

DEFAULT_EXPIRATION = 3600


class RedisCache(Cache):
    """Redis-backed application cache."""

    def __init__(self, client: Redis) -> None:
        """Initialize the adapter with a Redis client."""
        self._client = client

    async def set(self, key: str, value: Any, ex: int = DEFAULT_EXPIRATION) -> None:
        """Cache a value with an expiration."""
        await self._client.set(key, value, ex)

    async def get(self, key: str) -> Any:
        """Return a cached value."""
        return await self._client.get(key)
