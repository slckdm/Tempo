import asyncio
import logging

from dishka import make_async_container
from faststream.rabbit import RabbitBroker, RabbitExchange

from tempo_toolkit.infrastructure.cache import RedisSettings
from tempo_toolkit.infrastructure.database import PostgresProvider, PostgresSettings
from tempo_toolkit.infrastructure.messaging import MANAGEMENT_EXCHANGE, make_rabbit_broker

from app.core.commands.publish_outbox_messages import PublishOutboxMessages
from app.main.config.loader import (
    load_logging_settings,
    load_postgres_settings,
    load_rabbitmq_settings,
    load_redis_settings,
)
from app.main.ioc.outbound import OutboxProvider
from app.main.ioc.relay import RelayProvider
from app.main.setup import setup_logging
from app.outbound.sqlalchemy.mappings.all import map_tables


async def start_relay() -> None:
    logging_settings = load_logging_settings()
    setup_logging(level=logging_settings.LEVEL)

    rmq_settings = load_rabbitmq_settings()
    map_tables()

    broker = make_rabbit_broker(rmq_settings)
    await broker.connect()
    await broker.declare_exchange(MANAGEMENT_EXCHANGE)

    container = make_async_container(
        OutboxProvider(),
        RelayProvider(),
        PostgresProvider(),
        context={
            PostgresSettings: load_postgres_settings(),
            RabbitBroker: broker,
            RedisSettings: load_redis_settings(),
            RabbitExchange: MANAGEMENT_EXCHANGE
        },
    )

    logging.info("Starting publisher service")
    try:
        while True:
            async with container() as scope:
                relay = await scope.get(PublishOutboxMessages)
                await relay()
            await asyncio.sleep(1)
    finally:
        await broker.stop()
        await container.close()


if __name__ == "__main__":
    asyncio.run(start_relay())
