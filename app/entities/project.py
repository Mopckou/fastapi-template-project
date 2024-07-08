from pydantic import Field

from app.entities.base import BaseEntity
from app.entities.space import SpaceEntity


class ProjectEntity(BaseEntity):
    name: str = Field(..., title="Имя продукта", max_length=64, min_length=3)
    slug: str = Field(..., title="Идентификатор продукта", max_length=64, min_length=3)
    status: str = Field(...)
    space: list['SpaceEntity'] = Field(..., title="Пространство") # noqa
