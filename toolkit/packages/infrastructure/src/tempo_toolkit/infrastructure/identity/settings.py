"""Keycloak settings."""

from pydantic import BaseModel


class KeycloakSettings(BaseModel):
    """Keycloak connection settings."""

    URL: str
    REALM: str
    CLIENT_ID: str
    CLIENT_SECRET: str

    @property
    def token_url(self) -> str:
        """Return the OpenID Connect token endpoint."""
        return f"{self.URL}/realms/{self.REALM}/protocol/openid-connect/token"
