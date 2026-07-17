from unittest.mock import create_autospec

import pytest
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.healthcheck import Healthcheck, HealthTrouble


@pytest.mark.asyncio
async def test_healthcheck_success() -> None:
    session = create_autospec(AsyncSession, instance=True)
    broker = create_autospec(RabbitBroker, instance=True)
    await Healthcheck(session, broker)()

    session.scalar.assert_awaited_once()


@pytest.mark.asyncio
async def test_healthcheck_database_failure() -> None:
    session = create_autospec(AsyncSession, instance=True)
    broker = create_autospec(RabbitBroker, instance=True)
    session.scalar.side_effect = RuntimeError

    with pytest.raises(HealthTrouble):
        await Healthcheck(session, broker)()
