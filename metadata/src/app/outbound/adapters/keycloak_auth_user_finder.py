from toolkit.clients import KeycloakClient
from toolkit.entities import ServiceAccount, User
from toolkit.types_ import UserID

from app.core.commands.ports.auth_user_finder import AuthorizedUserFinder


class KeycloakAuthorizedUserFinder(AuthorizedUserFinder):
    def __init__(self, client: KeycloakClient) -> None:
        self._client = client

    async def get_by_id(self, id: UserID) -> User | ServiceAccount | None:
        user = await self._client.get_user_by_id(str(id))

        if not user:
            return None

        return User(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            first_name=user["firstName"],
            last_name=user["lastName"],
        )
