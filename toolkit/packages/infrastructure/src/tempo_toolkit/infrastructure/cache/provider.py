"""Redis Dishka provider."""

from dishka import Provider, Scope, provide
from redis.asyncio.client import Redis

from .settings import RedisSettings


class RedisClientProvider(Provider):
    """Provide an application-scoped Redis client."""

    @provide(scope=Scope.APP)
    def provide_redis_client(self, settings: RedisSettings) -> Redis:
        """Create a Redis client."""
        return Redis(
            host=settings.HOST,
            port=settings.PORT,
            db=settings.DB,
            password=settings.PASSWORD,
            decode_responses=True,
            encoding="utf-8",
        )
