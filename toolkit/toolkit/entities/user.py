"""Module: User Data DAO."""

from pydantic import BaseModel

from toolkit.types_ import UserID


class User(BaseModel):
    """User Data."""

    id: UserID
    username: str
    email: str | None = None
    first_name: str
    last_name: str
