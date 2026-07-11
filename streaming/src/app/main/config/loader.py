from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict

from toolkit.config.loader import load_settings
from toolkit.config.settings import (
    AppSettings,
    KeycloakSettings,
    LoggingSettings,
    RedisSettings,
    S3Settings,
)

BASE_DIR: Final[Path] = Path(__file__).resolve().parents[4]
_ENV_FILE: Final[Path] = BASE_DIR.joinpath(".env")

_DEFAULT_CONFIG_DICT: Final[SettingsConfigDict] = SettingsConfigDict(
    env_file=_ENV_FILE, extra="ignore"
)


class S3EnvConfig(BaseSettings, S3Settings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="S3_")


class KeycloakEnvConfig(BaseSettings, KeycloakSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="KEYCLOAK_")


class AppEnvConfig(BaseSettings, AppSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="APP_")


class LoggingEnvConfig(BaseSettings, LoggingSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="LOGGING_")


class RedisEnvConfig(BaseSettings, RedisSettings):
    model_config = _DEFAULT_CONFIG_DICT | SettingsConfigDict(env_prefix="Redis_")


def load_app_settings() -> AppSettings:
    return load_settings(AppEnvConfig)


def load_keycloak_settings() -> KeycloakSettings:
    return load_settings(KeycloakEnvConfig)


def load_s3_settings() -> S3Settings:
    return load_settings(S3EnvConfig)


def load_logging_settings() -> LoggingSettings:
    return load_settings(LoggingEnvConfig)


def load_redis_settings() -> RedisSettings:
    return load_settings(RedisEnvConfig)
