from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from toolkit.common.ports.transaction import Transaction
from toolkit.service.exceptions import TransactionError


class SQLATransaction(Transaction):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def commit(self) -> None:
        try:
            await self.__session.commit()
        except SQLAlchemyError as sqlalchemy_err:
            raise TransactionError from sqlalchemy_err

    async def rollback(self) -> None:
        try:
            await self.__session.rollback()
        except SQLAlchemyError as sqlalchemy_err:
            raise TransactionError from sqlalchemy_err
