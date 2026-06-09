"""Module: Keycloak configuration."""

from os import environ as env

from toolkit.security import KeycloakConfig

keycloak_config = KeycloakConfig(
    url=env["KEYCLOAK_URL"],
    realm=env["KEYCLOAK_SERVICE_REALM"],
    client_id=env["KEYCLOAK_SERVICE_CLIENT_ID"],
    client_secret=env["KEYCLOAK_SERVICE_CLIENT_SECRET"],
    token_url=(
        f"{env["KEYCLOAK_URL"]}/realms/{env["KEYCLOAK_SERVICE_REALM"]}"
        "/protocol/openid-connect/token"
    ),
)
