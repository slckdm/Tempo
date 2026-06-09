"""Module: Database config."""

from dataclasses import dataclass
from os import environ as env


@dataclass
class DBConfig:
    """Database configuration object."""

    host = env["DB_HOST"]
    port = env["DB_PORT"]
    name = env["DB_NAME"]
    user = env["DB_USER"]
    password = env["DB_PASS"]
