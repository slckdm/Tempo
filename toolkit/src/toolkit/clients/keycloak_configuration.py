"""Module: Keycloak Configuration."""

from dataclasses import dataclass


@dataclass
class KeycloakConfig:
    """Keycloak configuration object."""

    url: str
    realm: str
    client_id: str
    client_secret: str
    token_url: str
