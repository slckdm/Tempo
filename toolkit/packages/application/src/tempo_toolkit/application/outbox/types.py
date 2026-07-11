"""Transactional outbox value types."""

from enum import StrEnum
from typing import NewType
from uuid import UUID

OutboxMessageID = NewType("OutboxMessageID", UUID)


class AggregateType(StrEnum):
    """Base aggregate type for service-specific enumerations."""
