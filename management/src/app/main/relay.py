import asyncio

from dishka import make_async_container
from faststream.rabbit import RabbitBroker
from toolkit.messaging.broker import (
    MANAGEMENT_DLE,
    MANAGEMENT_DLQ,
    MANAGEMENT_EXCHANGE,
    make_rabbit_broker,
)

from app.core.commands.publish_outbox_messages import PublishOutboxMessages
from app.main.config.loader import (
    load_postgres_settings,
    load_rabbitmq_settings,
    load_redis_settings,
)
from app.main.config.settings import PostgresSettings, RedisSettings
from app.main.ioc.outbound import PostgresProvider
from app.main.ioc.relay import RelayProvider


async def start_relay() -> None:
    rmq_settings = load_rabbitmq_settings()

    broker = make_rabbit_broker(rmq_settings)
    await broker.connect()
    await broker.declare_exchange(MANAGEMENT_EXCHANGE)
    await broker.declare_exchange(MANAGEMENT_DLE)
    await broker.declare_queue(MANAGEMENT_DLQ)

    container = make_async_container(
        RelayProvider(),
        PostgresProvider(),
        context={
            PostgresSettings: load_postgres_settings(),
            RabbitBroker: broker,
            RedisSettings: load_redis_settings(),
        },
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
