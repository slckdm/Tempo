"""Keycloak identity integration."""

from .adapters import KeycloakAuthorizedUserFinder, KeycloakIdentityProvider
from .client import APIClientError, KeycloakClient, KeycloakConfig
from .jwt import (
    decode_token,
    get_service_account_data_from_token,
    get_user_data_from_token,
    normalize_public_key,
)
from .provider import KeycloakClientProvider
from .settings import KeycloakSettings

__all__ = [
    "APIClientError",
    "KeycloakAuthorizedUserFinder",
    "KeycloakClient",
    "KeycloakClientProvider",
    "KeycloakConfig",
    "KeycloakIdentityProvider",
    "KeycloakSettings",
    "decode_token",
    "get_service_account_data_from_token",
    "get_user_data_from_token",
    "normalize_public_key",
]
