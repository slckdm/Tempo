from pydantic import BaseModel, Field


class CompleteUploadResponseBody(BaseModel):

    urn: str = Field(
        description="The URN of the completed upload.",
        json_schema_extra={"example": "urn:upload:123"}
    )
