from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.ports.flusher import Flusher


class SQLAFlusher(Flusher):

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def flush(self, objects: Sequence[Any] | None = None) -> None:
        await self.__session.flush(objects)
