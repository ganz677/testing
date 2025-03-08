from typing import Annotated
from annotated_types import (
    MinLen,
    MaxLen
)
from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict
)


class CreateUser(BaseModel):
    username: Annotated[str, MaxLen(20), MinLen(2)]
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    is_active: bool = True