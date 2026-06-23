from io import IOBase


from pydantic import BaseModel, ConfigDict, Field, SkipValidation


class Object(BaseModel):

    body: SkipValidation[IOBase] = Field(alias="Body")
    content_range: int | None = Field(None, alias="ContentRange")
    content_length: int = Field(alias="ContentLength")
    content_type: str = Field(alias="ContentType")

    model_config = ConfigDict(arbitrary_types_allowed=True)
