import asyncio
import logging

from dishka import make_async_container
from dishka_faststream import FastStreamProvider, setup_dishka
from faststream import FastStream

from tempo_toolkit.infrastructure.cache import RedisSettings
from tempo_toolkit.infrastructure.database import PostgresSettings
from tempo_toolkit.infrastructure.identity import KeycloakSettings
from tempo_toolkit.infrastructure.messaging import (
    LIBRARY_DLE,
    LIBRARY_DLQ,
    make_rabbit_broker,
)

from app.inbound.amqp.router import router
from app.main.config.loader import (
    load_keycloak_settings,
    load_logging_settings,
    load_postgres_settings,
    load_rabbitmq_settings,
    load_redis_settings,
)
from app.main.ioc.consumer import ConsumerProvider
from app.main.ioc.outbound import KeycloakClientProvider, PostgresProvider, RedisClientProvider
from app.main.setup import setup_logging
from app.outbound.sqlalchemy.mappings.all import map_tables


async def create_app() -> None:
    logging_settings = load_logging_settings()
    setup_logging(level=logging_settings.LEVEL)
    map_tables()
    rmq_settings = load_rabbitmq_settings()

    broker = make_rabbit_broker(rmq_settings)
    await broker.connect()
    broker.include_router(router)
    await broker.declare_exchange(LIBRARY_DLE)
    await broker.declare_queue(LIBRARY_DLQ)

    app = FastStream(broker)

    container = make_async_container(
        FastStreamProvider(),
        ConsumerProvider(),
        KeycloakClientProvider(),
        RedisClientProvider(),
        PostgresProvider(),
        context={
            PostgresSettings: load_postgres_settings(),
            RedisSettings: load_redis_settings(),
            KeycloakSettings: load_keycloak_settings(),
        },
    )

    setup_dishka(container, app)

    logging.info("Starting consumer service")
    await app.run()


if __name__ == "__main__":
    asyncio.run(create_app())
