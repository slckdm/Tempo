from typing import Protocol, Sequence

from toolkit.types_ import UserID


class IdentityProvider(Protocol):
    async def get_current_user_id(self, audience: Sequence[str]) -> UserID: ...
