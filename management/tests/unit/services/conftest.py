from typing import cast
from unittest.mock import create_autospec

import pytest

from app.outbound.ports.auth_user_finder import AuthorizedUserFinder
from app.outbound.ports.identity_provider import IdentityProvider

from .mock_types import AuthorizedUserFinderMock, IdentityProviderMock


@pytest.fixture
def identity_provider() -> IdentityProvider:
    return IdentityProviderMock()


@pytest.fixture
def authorized_user_finder() -> AuthorizedUserFinder:
    return AuthorizedUserFinderMock()
