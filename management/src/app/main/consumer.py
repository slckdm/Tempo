import logging
import asyncio

from dishka import make_async_container
from dishka_faststream import FastStreamProvider, setup_dishka
from faststream import FastStream
from toolkit.messaging.broker import (
    MANAGEMENT_DLE,
    MANAGEMENT_DLQ,
    MANAGEMENT_EXCHANGE,
    make_rabbit_broker,
)

from app.inbound.amqp.router import router
from app.main.config.loader import (
    load_logging_settings,
    load_postgres_settings,
    load_rabbitmq_settings,
    load_redis_settings,
    load_s3_settings,
)
from app.main.config.settings import PostgresSettings, RedisSettings, S3Settings
from app.main.ioc.consumer import ConsumerProvider
from app.main.ioc.outbound import PostgresProvider, RedisClientProvider, S3Provider
from app.main.setup import setup_logging


async def create_app() -> None:
    logging_settings = load_logging_settings()
    setup_logging(level=logging_settings.LEVEL)

    rmq_settings = load_rabbitmq_settings()

    broker = make_rabbit_broker(rmq_settings)
    await broker.connect()
    broker.include_router(router)
    await broker.declare_exchange(MANAGEMENT_EXCHANGE)
    await broker.declare_exchange(MANAGEMENT_DLE)
    await broker.declare_queue(MANAGEMENT_DLQ)

    app = FastStream(broker)

    container = make_async_container(
        ConsumerProvider(),
        FastStreamProvider(),
        PostgresProvider(),
        RedisClientProvider(),
        S3Provider(),
        context={
            PostgresSettings: load_postgres_settings(),
            S3Settings: load_s3_settings(),
            RedisSettings: load_redis_settings(),
        },
    )

    setup_dishka(container, app)

    logging.info("Starting consumer service")
    await app.run()


if __name__ == "__main__":
    asyncio.run(create_app())
