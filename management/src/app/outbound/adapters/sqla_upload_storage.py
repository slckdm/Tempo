from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.ports.upload_storage import UploadStorage
from app.core.models import Upload


class SQLAUploadStorage(UploadStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, upload: Upload) -> None:
        self.__session.add(upload)

    async def get_by_id(self, id: UUID, for_update: bool = False) -> Upload | None:
        return await self.__session.get(Upload, id, with_for_update=for_update)

    async def delete(self, upload: Upload) -> None:
        await self.__session.delete(upload)
