from typing import Any, Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.ports.flusher import Flusher
from app.outbound.exceptions import FlusherError


class SQLAFlusher(Flusher):

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def flush(self, objects: Sequence[Any] | None = None) -> None:
        try:
            await self.__session.flush(objects)
        except SQLAlchemyError as sqlalchemy_err:
            raise FlusherError from sqlalchemy_err
