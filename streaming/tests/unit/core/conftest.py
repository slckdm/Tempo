from typing import cast
from unittest.mock import create_autospec

import pytest

from tempo_toolkit.application.auth import AuthorizedUserFinder, IdentityProvider
from tempo_toolkit.application.storage import ObjectStorage

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
