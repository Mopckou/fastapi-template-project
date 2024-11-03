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
        parent_table = select(SpaceModel).where(SpaceModel.id == id).cte("parent_table", recursive=True)

        q = parent_table.union(
            select(parent_alias).join(
                parent_table, parent_table.c.parent_id == parent_alias.id
            )
        )
        r = aliased(SpaceModel, alias=q)  # этот элиас позволяет вывести объекты в результате
        result = (await self._session.scalars(
            select(r)
        )).unique().all()

        dicts = {elem.id: elem for elem in result}

        return to_three(id, dicts)


def to_three(id: int, spaces: dict[int, SpaceModel]):
    spaces_models = {
        int(model.id): SpaceEntity(**vars(model)) for model in spaces.values()
    }

    for i, v in spaces.items():

        if v.parent_id not in spaces_models:
            continue

        parent_space = spaces_models.get(v.parent_id)
        if not parent_space:
            raise Exception("Model is empty")

        current_model = spaces_models.get(v.id)
        if not current_model:
            raise Exception("Model is not found")

        current_model.parent = parent_space

    return spaces_models[id]
