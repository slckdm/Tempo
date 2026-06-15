"""Module: Get Current User Data Utility."""

from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, Request
from fastapi.exceptions import HTTPException

from jwt.exceptions import ExpiredSignatureError

from toolkit.clients import KeycloakClient
from toolkit.entities import ServiceAccount, User
from toolkit.security.utils import decode_token, normalize_public_key

from app.common.security.oauth2_scheme import oauth2_scheme
from app.main.config.loader import load_keycloak_settings


async def get_current_user(request: Request) -> User:
    """Get current user dependency.

    Dependencies:
        token [str, Depends(oauth2_scheme)]: Current request token.

    Returns:
        User: User data object.
    """
    token = await oauth2_scheme(request)
    if not token:
        raise HTTPException(HTTPStatus.UNAUTHORIZED)
    keycloak_client = KeycloakClient(keycloak_config)
    try:
        user = decode_token(token, normalize_public_key(await keycloak_client.get_jwk()))
    except ExpiredSignatureError as expired_exception:
        raise HTTPException(HTTPStatus.FORBIDDEN) from expired_exception
    if isinstance(user, ServiceAccount):
        raise HTTPException(HTTPStatus.FORBIDDEN)
    return user
