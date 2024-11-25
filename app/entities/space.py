from __future__ import annotations

from app.entities.base import BaseEntity


class SpaceEntity(BaseEntity):
    id: int
    name: str
    parent: SpaceEntity | None
