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
        # parent_table_alias = aliased(SpaceModel, parent_table, name='p')
        q = parent_table.union(
            select(parent_alias).join(
                parent_table, parent_table.c.id == parent_alias.parent_id
            )
        )
        r = aliased(SpaceModel, alias=q)  # этот элиас позволяет вывести объекты в результате
        result = (await self._session.scalars(
            select(r)
        )).unique().all()
        # spaces = [SpaceEntity(**vars(model)) for model in result] эти данные нужно построить в виде дерева
        dicts = {elem.id: elem for elem in result}
        print([SpaceEntity(**vars(model)) for model in result])
        print(dicts)
        return to_three(id, dicts)


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


def to_three(id: int, spaces: dict[int, SpaceModel]):
    spaces_models = {
        int(model.id): SpaceEntity(**vars(model)) for model in spaces.values()
    }
    print(spaces_models)
    while 1:
        if len(spaces_models) == 1:
            return spaces_models[id]

        for i, v in spaces.items():
            print(i, v)
            if i not in spaces_models:
                continue

            if v.parent_id not in spaces_models:
                continue

            parent_space = spaces_models.get(v.parent_id)
            if not parent_space:
                raise Exception("Model is empty")

            current_model = spaces_models.get(i)
            if current_model:
                current_model.parent = parent_space

            spaces_models.pop(i)


def req_print(obj, p="->"):
    try:
        print(p, obj.id, obj.name)
        if obj.parent is None:
            return
        req_print(obj.parent, "-" + p)
    except Exception as e:
        print(e)
        return

