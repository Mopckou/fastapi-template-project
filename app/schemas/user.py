from uuid import UUID

from pydantic import BaseModel, Field

from app.entities.user import UserEntity
from app.schemas.base import BaseResponse


class UserRequest(BaseModel):
    email: str = Field(..., title="user email", max_length=64, min_length=3)
    first_name: str = Field(..., title="user name", max_length=64, min_length=3)
    middle_name: str | None = Field(..., title="middle name", max_length=64, min_length=3)
    last_name: str | None = Field(..., title="last name", max_length=64, min_length=3)
    password: str = Field(..., title="user password", max_length=50, min_length=7)


class NewUserID(BaseModel):
    id: UUID = Field(..., title="user ID")


class NewUserResponse(BaseResponse):
    result: NewUserID


class UserResponse(BaseResponse):
    result: UserEntity


class UsersResponse(BaseResponse):
    result: list[UserEntity]
