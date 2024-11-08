from abc import abstractmethod
from typing import Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.space import SpaceEntity
from app.models.space import SpaceModel
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

        return await self.map_to_entity(result)

    async def map_to_entity(self, model: SpaceModel | None) -> SpaceEntity | None:
        if not model:
            return None

        parent = await model.awaitable_attrs.parent

        return SpaceEntity(
            id=model.id,
            name=model.name,
            parent=await self.map_to_entity(parent)
        )
