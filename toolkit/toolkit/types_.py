from typing import Any, NewType, Self
from uuid import UUID

from pydantic_core import core_schema

UserID = NewType("UserID", UUID)

UserToken = NewType("UserToken", str)


class URNType[T]:
    prefix: str = "urn"
    delimiter: str = ":"
    namespace: str

    def __init__(self, id: T) -> None:
        self.__id = id

    @property
    def id(self) -> T:
        return self.__id

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.delimiter.join((self.prefix, self.namespace, str(self.id)))

    @classmethod
    def __validate(cls, value: Any) -> str:
        _value = str(value).split(cls.delimiter)
        if len(_value) != 3:
            raise ValueError(f"Wrong URN value: {value}")

        prefix, namespace, id = _value

        if namespace != cls.namespace or prefix != cls.prefix:
            raise ValueError(f"Wrong URN value: {value}")

        return id

    @classmethod
    def from_string(cls, value: str) -> Self:
        return cls(id=cls.__validate(value))

    @classmethod
    def __get_pydantic_core_schema__(
        cls, *args, **kwargs
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.no_info_after_validator_function(
            lambda value: value if isinstance(value, cls) else cls(id=cls.__validate(value)),
            schema=core_schema.any_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda value: str(value)
            )
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, *_) -> dict[str, str]:
        return {
            "type": "string",
            "title": "URN",
            "description": "Uniform Resource Name",
            "example": cls.delimiter.join([cls.prefix, cls.namespace, "1"]),
        }
