from __future__ import annotations

from pydantic import Field

from app.entities.base import BaseEntity


class SpaceEntity(BaseEntity):
    id: int = Field(...)
    name: str = Field(..., title="Имя проекта", max_length=64, min_length=3)
    parent: SpaceEntity | None = Field(alias='parent', default=None, exclude=True) #  exclude нужен чтобы не было циклической ошибки преобразования в json
    children: list[SpaceEntity] = Field(alias='children', default=[])

    # projects: list['ProjectEntity'] = Field(..., title="Проекты в пространстве")  # noqa
