"""Module: OAuth2 authentication flow schema."""

from fastapi.security import OAuth2PasswordBearer

from app.main.config.loader import load_keycloak_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=load_keycloak_settings().token_url)
