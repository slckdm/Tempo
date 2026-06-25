from typing import Protocol

from toolkit.entities import ServiceAccount, User
from toolkit.types_ import UserID


class AuthorizedUserFinder(Protocol):
    async def get_by_id(self, id: UserID) -> User | ServiceAccount | None: ...
