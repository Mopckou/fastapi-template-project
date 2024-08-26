from abc import abstractmethod
from typing import Union, Iterator
from uuid import UUID

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, selectinload, query, Mapped

from app.entities.space import SpaceEntity
from app.models.space import SpaceModel
from app.repositories.base import BaseRepository, IRepositoryBase


class ISpaceRepository(IRepositoryBase):
    @abstractmethod
    async def create(self, *args, **kwargs) -> SpaceEntity:
        raise NotImplementedError()


class SpaceRepository(BaseRepository, ISpaceRepository):
    __table_cls__ = SpaceModel
    __entity_model__ = SpaceEntity

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, name: str, slug: str, parent_space_id: int) -> SpaceEntity:
        project = SpaceModel(
            name=name,
            slug=slug,
        )

        self._session.add(project)
        await self._session.flush()

        return SpaceEntity(**vars(project))

    async def get_by_id(self, id: Union[int, UUID]) -> SpaceEntity | None:
        parent_alias = aliased(SpaceModel, name='s')
        result = (await self._session.scalars(
            select(SpaceModel).options(
                # selectinload(SpaceModel.children, recursion_depth=1),  # Это если нужно показать наследников
                selectinload(SpaceModel.parent, recursion_depth=1),  # проверить как работает глубина рекурсии
            ).where(SpaceModel.id == id).join(SpaceModel.parent.of_type(parent_alias), full=True)

        )).unique().all()

        return result[0] if len(result) > 0 else None


def map_entities_to_three(next_id: int, spaces: dict[int, SpaceModel]):
    if next_id is None:
        return

    if next_id not in spaces:
        return

    space_model = spaces.get(next_id)
    if not space_model:
        raise Exception("Model is empty")

    space = SpaceEntity(**vars(space_model))

    space_entity_parent = map_entities_to_three(int(space_model.parent_id), spaces)
    space.parent = space_entity_parent

    return space
