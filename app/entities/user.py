from uuid import UUID

from pydantic import Field

from app.entities.base import BaseEntity


class PasswordEntity(BaseEntity):
    id: int = Field(...)
    hash: str = Field(...)


class UserEntity(BaseEntity):

    id: UUID = Field(..., title="user ID")
    email: str = Field(..., title="user email")
    first_name: str = Field(..., title="first name")
    middle_name: str | None = Field(..., title="middle name")
    last_name: str | None = Field(..., title="last name")
