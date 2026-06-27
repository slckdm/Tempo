"""Module: Service Account DAO."""

from pydantic import BaseModel


class ServiceAccount(BaseModel):
    """Service Account Data."""

    client_id: str
    preferred_username: str
