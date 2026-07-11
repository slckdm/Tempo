"""Framework-independent application tests."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from tempo_toolkit.application.auth import CurrentUserService, User
from tempo_toolkit.application.errors import Unauthorized
from tempo_toolkit.application.outbox import AggregateType, OutboxService
from tempo_toolkit.contracts.events import MetadataReadyEvent
from tempo_toolkit.contracts.identifiers import UserID
from tempo_toolkit.contracts.routing import METADATA_READY_RK
from tempo_toolkit.contracts.uploads import UploadURN


class StubAggregateType(AggregateType):
    """Aggregate type used by the outbox test."""

    UPLOAD = "upload"


class FixedTimer:
    """Fixed UTC timer."""

    now = datetime(2026, 7, 11, tzinfo=UTC)


@pytest.mark.asyncio
async def test_current_user_service_returns_authorized_user() -> None:
    """The current-user service resolves a verified principal."""
    user = User(
        id=UserID(uuid4()),
        username="listener",
        email=None,
        first_name="Tempo",
        last_name="User",
    )
    identity_provider = AsyncMock()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder = AsyncMock()
    authorized_user_finder.get_by_id.return_value = user

    service = CurrentUserService(identity_provider, authorized_user_finder)

    assert await service.get_current_user(["tempo:etc"]) == user


@pytest.mark.asyncio
async def test_current_user_service_rejects_missing_user() -> None:
    """A missing authorized principal is rejected."""
    identity_provider = AsyncMock()
    identity_provider.get_current_user_id.return_value = UserID(uuid4())
    authorized_user_finder = AsyncMock()
    authorized_user_finder.get_by_id.return_value = None

    with pytest.raises(Unauthorized):
        await CurrentUserService(identity_provider, authorized_user_finder).get_current_user([])


@pytest.mark.asyncio
async def test_outbox_service_serializes_event() -> None:
    """The outbox service stores the stable event wire payload."""
    upload_id = UploadURN(uuid4())
    message = await OutboxService(FixedTimer()).create_message(
        StubAggregateType.UPLOAD,
        str(upload_id),
        METADATA_READY_RK,
        MetadataReadyEvent(upload_id=upload_id),
    )

    assert message.aggregate_type == "upload"
    assert message.event_type == "rk.tempo.md.metadata.ready"
    assert message.payload["upload_id"] == str(upload_id)
    assert message.created_at == FixedTimer.now
