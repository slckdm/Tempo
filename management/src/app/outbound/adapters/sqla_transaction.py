from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.ports.transaction import Transaction


class SQLATransaction(Transaction):

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def commit(self) -> None:
        await self.__session.commit()
