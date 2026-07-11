"""Web application settings."""

from pydantic import BaseModel


class AppSettings(BaseModel):
    """FastAPI application settings."""

    NAME: str
    HOST: str
    PORT: int
    DEBUG: bool = False
    ALLOWED_ORIGINS: list[str]
