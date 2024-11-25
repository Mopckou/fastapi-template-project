from abc import abstractmethod
from typing import Union, Iterator
from uuid import UUID

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, selectinload, query, Mapped, immediateload

from app.entities.space import SpaceEntity
from app.models.space import SpaceModel, DEPTH
from app.repositories.base import BaseRepository, IRepositoryBase


class ISpaceRepository(IRepositoryBase):
    @abstractmethod
    async def create(self, name: str, parent_space_id: int) -> SpaceEntity:
        raise NotImplementedError()


class SpaceRepository(BaseRepository, ISpaceRepository):
    __table_cls__ = SpaceModel
    __entity_model__ = SpaceEntity

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, name: str, parent_space_id: int) -> SpaceEntity:
        space = SpaceModel(
            name=name,
            parent_id=parent_space_id
        )

        self._session.add(space)
        await self._session.flush()

        return SpaceEntity(
            id=space.id,
            name=space.name,
        )

    async def get_by_id(self, id: Union[int, UUID]) -> SpaceEntity | None:
        result = (await self._session.scalars(
            select(SpaceModel).where(SpaceModel.id == id)
        )).unique().one_or_none()

        return await map_to_entity(result, DEPTH)


async def map_to_entity(model: SpaceModel | None, depth: int) -> SpaceEntity | None:
    if not model:
        return None

    if depth == 0:
        parent_model = await model.awaitable_attrs.parent
        parent_entity = await map_to_entity(parent_model, DEPTH)
    else:
        parent_entity = await map_to_entity(model.parent, depth - 1)

    return SpaceEntity(
        id=model.id,
        name=model.name,
        parent=parent_entity
    )
