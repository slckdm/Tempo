"""Module: User Data DTO."""

from pydantic import BaseModel


class User(BaseModel):
    """User Data."""

    id: str
    username: str
    email: str | None = None
    first_name: str
    last_name: str
