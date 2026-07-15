from faststream.rabbit import RabbitBroker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class HealthTrouble(Exception):
    ...


class Healthcheck:

    def __init__(self, session: AsyncSession, broker: RabbitBroker) -> None:
        self._session = session
        self._broker = broker

    async def __call__(self) -> None:
        try:
            await self.__check_db(self._session)
            await self.__check_broker(self._broker)
        except Exception as err:
            raise HealthTrouble from err

    async def __check_db(self, session: AsyncSession) -> None:
        await session.scalar(select(1))


    async def __check_broker(self, broker: RabbitBroker) -> None:
        await broker.ping(10)
