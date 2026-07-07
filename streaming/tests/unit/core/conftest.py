from typing import cast
from unittest.mock import create_autospec

import pytest

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.queries.ports.object_storage import ObjectStorage
from tests.unit.core.mock_types import (
    AuthorizedUserFinderMock,
    IdentityProviderMock,
    ObjectStorageMock,
)


@pytest.fixture
def identity_provider() -> IdentityProvider:
    return cast(IdentityProviderMock, create_autospec(IdentityProvider, instance=True))


@pytest.fixture
def object_storage() -> ObjectStorage:
    return cast(ObjectStorageMock, create_autospec(ObjectStorage, instance=True))

@pytest.fixture
def authorized_user_finder() -> "AuthorizedUserFinder":
    return cast(AuthorizedUserFinderMock, create_autospec(AuthorizedUserFinder, instance=True))
