from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict

from .settings import (
    AppSettings,
    KeycloakSettings,
    S3Settings,
)

BASE_DIR: Final[Path] = Path(__file__).resolve().parents[4]
_ENV_FILE: Final[Path] = BASE_DIR.joinpath(".env")

_DEFAULT_CONFIG_DICT: Final[SettingsConfigDict] = SettingsConfigDict(
    env_file=_ENV_FILE, extra="ignore"
)


def _load_settings[E: BaseSettings](env_cls: type[E]) -> E:
    return env_cls()

class S3EnvConfig(BaseSettings, S3Settings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="S3_")


class KeycloakEnvConfig(BaseSettings, KeycloakSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="KEYCLOAK_")


class AppEnvConfig(BaseSettings, AppSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="APP_")


def load_app_settings() -> AppSettings:
    return _load_settings(AppEnvConfig)


def load_keycloak_settings() -> KeycloakSettings:
    return _load_settings(KeycloakEnvConfig)


def load_s3_settings() -> S3Settings:
    return _load_settings(S3EnvConfig)
