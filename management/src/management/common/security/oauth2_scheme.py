"""Module: OAuth2 authentication flow schema."""

from fastapi.security import OAuth2PasswordBearer

from management.core.configs import keycloak_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=keycloak_config.token_url)
