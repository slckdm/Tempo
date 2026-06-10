"""Module: Authorization Strategy Abstract Base Class."""

from abc import ABC, abstractmethod


class AbstractAuthorizationStrategy(ABC):
    """Abstraction class for authorization strategies implementations."""

    @abstractmethod
    def get_headers(self) -> dict:
        """Get authorization headers."""
