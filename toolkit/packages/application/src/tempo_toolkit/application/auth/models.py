"""Authenticated principal models."""

from dataclasses import dataclass

from tempo_toolkit.contracts.identifiers import UserID


@dataclass(frozen=True, slots=True, kw_only=True)
class Account:
    """Authenticated account base model."""


@dataclass(frozen=True, slots=True, kw_only=True)
class User(Account):
    """Authenticated user."""

    id: UserID
    username: str
    email: str | None = None
    first_name: str
    last_name: str


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceAccount(Account):
    """Authenticated service account."""

    client_id: str
    preferred_username: str
