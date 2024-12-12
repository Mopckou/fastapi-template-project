from __future__ import annotations

from pydantic import Field

from app.entities.base import BaseEntity


class SpaceEntity(BaseEntity):
    id: int = Field(...)
    name: str = Field(..., title="Имя проекта", max_length=64, min_length=3)
    parent: SpaceEntity | None = Field(default=None)
