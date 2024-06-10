from typing import Any

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):

    result: dict | list[dict] | None = None
    errors: list[dict[str, Any]] = []


class OkResponse(BaseResponse):
    result: dict | None = Field(..., default_factory=dict)
