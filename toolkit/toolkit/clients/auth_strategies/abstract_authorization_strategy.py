
from abc import ABC, abstractmethod

class AbstractAuthorizationStrategy(ABC):

    @abstractmethod
    def get_headers(self) -> dict:
        ...
