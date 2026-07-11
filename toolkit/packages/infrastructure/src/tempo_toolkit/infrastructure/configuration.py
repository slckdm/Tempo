"""Environment configuration helpers."""

from pydantic_settings import BaseSettings


def load_settings[E: BaseSettings](environment_type: type[E]) -> E:
    """Instantiate an environment-backed settings model."""
    return environment_type()
