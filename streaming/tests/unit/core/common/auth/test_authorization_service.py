from unittest.mock import AsyncMock, Mock

import pytest

from tests.unit.core.factories import create_authorization_service


@pytest.mark.asyncio
async def test_get_token_returns_first_available() -> None:
    request = Mock()
    empty_schema = AsyncMock(return_value=None)
    token_schema = AsyncMock(return_value="rawtoken")
    service = create_authorization_service(request, [empty_schema, token_schema])

    token = await service.get_token()

    assert token == "rawtoken"
    empty_schema.assert_awaited_once_with(request)
    token_schema.assert_awaited_once_with(request)


@pytest.mark.asyncio
async def test_get_token_none_when_all_schemas_empty() -> None:
    request = Mock()
    schemas = [AsyncMock(return_value=None), AsyncMock(return_value=None)]
    service = create_authorization_service(request, schemas)

    assert await service.get_token() is None
