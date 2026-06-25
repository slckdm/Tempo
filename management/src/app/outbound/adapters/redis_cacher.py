from typing import Any

from redis.asyncio.client import Redis

from app.core.common.ports.cacher import Cacher

DEFAULT_EXPIRATION = 3600


class RedisCacher(Cacher):

    def __init__(self, client: Redis) -> None:
        self._client: Redis = client

    async def set(self, key: str, value: Any, ex: int = DEFAULT_EXPIRATION) -> None:
        await self._client.set(key, value, ex)

    async def get(self, key: str) -> Any:
        return await self._client.get(key)
