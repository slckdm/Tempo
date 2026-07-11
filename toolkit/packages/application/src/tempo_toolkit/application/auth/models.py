"""Authenticated principal models."""

from pydantic import BaseModel

from tempo_toolkit.contracts.identifiers import UserID


class User(BaseModel):
    """Authenticated user."""

    id: UserID
    username: str
    email: str | None = None
    first_name: str
    last_name: str


class ServiceAccount(BaseModel):
    """Authenticated service account."""

    client_id: str
    preferred_username: str
