"""Module: Get Current User Data Utility."""

from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException

from toolkit.security import KeycloakClient
from toolkit.security.models import ServiceAccount, User

from management.common.security.oauth2_scheme import oauth2_scheme
from management.core.configs import keycloak_config


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Get current user dependency.

    Dependencies:
        token [str, Depends(oauth2_scheme)]: Current request token.

    Returns:
        User: User data object.
    """
    user = await KeycloakClient(keycloak_config).decode_token(token)
    if isinstance(user, ServiceAccount):
        raise HTTPException(409, "Forbidden")
    return user
