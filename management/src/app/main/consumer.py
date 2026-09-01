import asyncio
import logging

from dishka import make_async_container
from dishka_faststream import FastStreamProvider, setup_dishka
from faststream import FastStream

from tempo_toolkit.infrastructure.cache import RedisClientProvider, RedisSettings
from tempo_toolkit.infrastructure.database import PostgresProvider, PostgresSettings
from tempo_toolkit.infrastructure.messaging import (
    MANAGEMENT_DLE,
    MANAGEMENT_DLQ,
    make_rabbit_broker,
)
from tempo_toolkit.infrastructure.messaging.settings import RabbitMQSettings
from tempo_toolkit.infrastructure.object_storage import S3Provider, S3Settings

from app.inbound.amqp.v1_router import make_v1_router
from app.main.config.loader import (
    load_logging_settings,
    load_postgres_settings,
    load_rabbitmq_settings,
    load_redis_settings,
    load_s3_settings,
)
from app.main.ioc.consumer import ConsumerProvider
from app.main.ioc.outbound import BrokerProvider, OutboxProvider
from app.main.setup import setup_logging
from app.outbound.sqlalchemy.mappings.all import map_tables


async def create_app() -> None:
    logging_settings = load_logging_settings()
    setup_logging(level=logging_settings.LEVEL)

    rmq_settings = load_rabbitmq_settings()
    map_tables()
    broker = make_rabbit_broker(rmq_settings)
    await broker.connect()
    broker.include_router(make_v1_router())
    await broker.declare_exchange(MANAGEMENT_DLE)
    await broker.declare_queue(MANAGEMENT_DLQ)

    app = FastStream(broker)

    container = make_async_container(
        OutboxProvider(),
        BrokerProvider(),
        ConsumerProvider(),
        FastStreamProvider(),
        PostgresProvider(),
        RedisClientProvider(),
        S3Provider(),
        context={
            PostgresSettings: load_postgres_settings(),
            S3Settings: load_s3_settings(),
            RedisSettings: load_redis_settings(),
            RabbitMQSettings: rmq_settings,
        },
    )

    setup_dishka(container, app)

    logging.info("Starting consumer service")
    await app.run()


if __name__ == "__main__":
    asyncio.run(create_app())
