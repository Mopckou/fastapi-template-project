from pydantic import BaseModel, Field


class User(BaseModel):
    email: str = Field(..., title="User email", max_length=64, min_length=3)
    first_name: str = Field(..., title="User first name", max_length=64, min_length=3)
    middle_name: str = Field(..., title="User middle name", max_length=64, min_length=3)
    last_name: str = Field(..., title="User last name", max_length=64, min_length=3)
