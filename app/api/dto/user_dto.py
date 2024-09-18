import uuid as uuid_v4

from pydantic import BaseModel, Field


class UserDto(BaseModel):
    uuid: uuid_v4.UUID = Field(description="User ID")
    name: str | None = Field(description="The name of the user")
    email: str = Field(description="The email of the user")
