from typing import Protocol
from unittest.mock import AsyncMock


class IdentityProviderMock:
    get_current_user_id: AsyncMock


class AuthorizedUserFinderMock:
    get_by_id: AsyncMock


class ObjectStorageMock(Protocol):
    get_object: AsyncMock
    put_object: AsyncMock
