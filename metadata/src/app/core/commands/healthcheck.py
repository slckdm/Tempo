"""Service healthcheck command."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class HealthTrouble(Exception):
    """Raised when a service dependency is unavailable."""


class Healthcheck:
    """Check whether the metadata service dependencies are available."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the command."""
        self._session = session

    async def __call__(self) -> None:
        """Check the database connection."""
        try:
            await self._session.scalar(select(1))
        except Exception as exception:
            raise HealthTrouble from exception
