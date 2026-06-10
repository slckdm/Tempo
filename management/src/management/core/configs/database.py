"""Module: Database config."""

from dataclasses import dataclass
from os import environ as env


@dataclass
class DBConfig:
    """Database configuration object."""

    host: str = env["DB_HOST"]
    port: int = int(env["DB_PORT"])
    name: str = env["DB_NAME"]
    user: str = env["DB_USER"]
    password: str = env["DB_PASS"]
    engine: str = "postgresql+asyncpg"

    url = f"{engine}://{user}:{password}@{host}:{port}/{name}"
