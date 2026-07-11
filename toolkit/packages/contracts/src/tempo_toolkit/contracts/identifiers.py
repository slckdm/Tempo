"""Shared identifiers."""

from typing import Any, NewType, Self
from uuid import UUID

from pydantic_core import core_schema

UserID = NewType("UserID", UUID)


class URN[T]:
    """Base Uniform Resource Name value object."""

    prefix: str = "urn"
    delimiter: str = ":"
    namespace: str

    def __init__(self, id: T) -> None:
        """Initialize a URN from its underlying identifier."""
        self.__identifier = id

    @property
    def id(self) -> T:
        """Return the underlying identifier."""
        return self.__identifier

    def __repr__(self) -> str:
        """Return the wire representation."""
        return str(self)

    def __str__(self) -> str:
        """Return the wire representation."""
        return self.delimiter.join((self.prefix, self.namespace, str(self.id)))

    @classmethod
    def _validate(cls, value: Any) -> str:
        parts = str(value).split(cls.delimiter)
        if len(parts) != 3:
            raise ValueError(f"Wrong URN value: {value}")

        prefix, namespace, identifier = parts
        if namespace != cls.namespace or prefix != cls.prefix:
            raise ValueError(f"Wrong URN value: {value}")

        return identifier

    @classmethod
    def from_string(cls, value: str) -> Self:
        """Create a URN from its string representation."""
        return cls(id=cls._validate(value))

    @classmethod
    def __get_pydantic_core_schema__(
        cls, *args: Any, **kwargs: Any
    ) -> core_schema.AfterValidatorFunctionSchema:
        """Return the Pydantic validation and serialization schema."""
        return core_schema.no_info_after_validator_function(
            lambda value: value if isinstance(value, cls) else cls(id=cls._validate(value)),
            schema=core_schema.any_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, *_: Any) -> dict[str, str]:
        """Return the JSON schema for a URN."""
        return {
            "type": "string",
            "title": "URN",
            "description": "Uniform Resource Name",
            "example": cls.delimiter.join([cls.prefix, cls.namespace, "1"]),
        }
