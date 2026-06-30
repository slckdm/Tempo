"""Module: OAuth2 authentication flow schema."""
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer

from app.main.config.loader import load_keycloak_settings

ACCESS_TOKEN_COOKIE = "access_token"


def get_oauth2_schema(*args) -> OAuth2PasswordBearer:
    return OAuth2PasswordBearer(tokenUrl=load_keycloak_settings().token_url, auto_error=False)


def get_cookie_schema(*args) -> APIKeyCookie:
    return APIKeyCookie(name=ACCESS_TOKEN_COOKIE, auto_error=False)
