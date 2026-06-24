from dishka import Provider, Scope, provide
from redis.asyncio.client import Redis

from app.main.config.settings import RedisSettings


class RedisClientProvider(Provider):

    @provide(scope=Scope.APP)
    def provide_redis_client(self, settings: RedisSettings) -> Redis:
        client = Redis(
            host=settings.HOST,
            port=settings.PORT,
            db=settings.DB,
            password=settings.PASSWORD,
            decode_responses=True,
            encoding="utf-8",
        )

        return client
