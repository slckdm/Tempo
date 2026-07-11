"""Infrastructure integration unit tests."""

from http import HTTPStatus
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from tempo_toolkit.application.auth import Token
from tempo_toolkit.application.errors import NotFound
from tempo_toolkit.infrastructure.database import make_outbox_message_table
from tempo_toolkit.infrastructure.identity import KeycloakIdentityProvider, normalize_public_key
from tempo_toolkit.infrastructure.identity import adapters as identity_adapters
from tempo_toolkit.infrastructure.messaging import MANAGEMENT_EXCHANGE
from tempo_toolkit.infrastructure.web import FastAPITokenProvider, JSendFailHandler


@pytest.mark.asyncio
async def test_fastapi_token_provider_uses_first_available_token() -> None:
    """FastAPI token extraction checks configured schemes in order."""
    missing_schema = AsyncMock(return_value=None)
    bearer_schema = AsyncMock(return_value="token")
    provider = FastAPITokenProvider(Mock(), [missing_schema, bearer_schema])

    assert await provider.get_token() == Token("token")


@pytest.mark.asyncio
async def test_keycloak_identity_provider_uses_cached_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Identity resolution does not refetch a cached realm key."""
    user_id = uuid4()
    client = Mock()
    client.get_jwk = AsyncMock()
    token_provider = Mock()
    token_provider.get_token = AsyncMock(return_value=Token("token"))
    cache = Mock()
    cache.get = AsyncMock(return_value="realm-key")
    cache.set = AsyncMock()
    monkeypatch.setattr(
        identity_adapters,
        "decode_token",
        lambda *args: {
            "sub": str(user_id),
            "given_name": "Tempo",
            "family_name": "User",
            "preferred_username": "listener",
            "email": "listener@example.com",
        },
    )

    provider = KeycloakIdentityProvider(client, token_provider, cache)

    assert await provider.get_current_user_id(["tempo:etc"]) == user_id
    client.get_jwk.assert_not_awaited()


@pytest.mark.asyncio
async def test_jsend_fail_handler_preserves_wire_shape() -> None:
    """FastAPI errors retain the existing JSend payload."""
    response = await JSendFailHandler(HTTPStatus.NOT_FOUND)(Mock(), NotFound())

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.body == b'{"data":{},"message":"Not Found","status":"fail"}'


def test_outbox_table_keeps_partial_index() -> None:
    """The outbox table keeps its unpublished-message partial index."""
    from sqlalchemy import orm

    table = make_outbox_message_table(orm.registry())
    index = next(iter(table.indexes))

    assert index.name == "ix_outbox_messages_unpublished_id"
    assert str(index.dialect_options["postgresql"]["where"]) == "published_at IS NULL"


def test_rabbitmq_topology_and_public_key_format_are_stable() -> None:
    """Infrastructure constants retain their external values."""
    assert MANAGEMENT_EXCHANGE.name == "tempo.management.exchange"
    assert normalize_public_key("key") == (
        "-----BEGIN PUBLIC KEY-----\n key \n-----END PUBLIC KEY-----"
    )
