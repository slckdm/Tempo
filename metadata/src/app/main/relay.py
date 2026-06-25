import asyncio

from dishka import make_async_container
from faststream.rabbit import RabbitBroker

from toolkit.messaging.broker import (
    METADATA_DLE,
    METADATA_DLQ,
    METADATA_EXCHANGE,
    make_rabbit_broker,
)

from app.core.commands.publish_outbox_messages import PublishOutboxMessages
from app.main.config.loader import load_postgres_settings, load_rabbitmq_settings
from app.main.config.settings import PostgresSettings
from app.main.ioc.outbound import get_outbound_providers
from app.main.ioc.relay import RelayProvider


async def start_relay() -> None:
    rmq_settings = load_rabbitmq_settings()
    postgres_settings = load_postgres_settings()

    broker = make_rabbit_broker(rmq_settings)
    await broker.connect()
    await broker.declare_exchange(METADATA_EXCHANGE)
    await broker.declare_exchange(METADATA_DLE)
    await broker.declare_queue(METADATA_DLQ)

    container = make_async_container(
        RelayProvider(),
        *get_outbound_providers(),
        context={PostgresSettings: postgres_settings, RabbitBroker: broker},
    )

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
