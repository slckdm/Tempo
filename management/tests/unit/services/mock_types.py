from toolkit.entities import User, ServiceAccount
from .factories import create_user
from toolkit.types_ import UserID
import random


class IdentityProviderMock:
    # get_current_user_id: AsyncMock

    async def get_current_user_id(self) -> UserID:
        return random.choice(AuthorizedUserFinderMock._users).id


class AuthorizedUserFinderMock:
    # get_by_id: AsyncMock
    _users = [create_user(), create_user(), create_user()]
    _users_map = {user.id: user for user in _users}

    async def get_by_id(self, id: UserID) -> User | ServiceAccount | None:
        return self._users_map.get(id)
