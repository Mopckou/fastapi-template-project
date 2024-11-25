from abc import abstractmethod

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def get_by_id(self, id: int) -> SpaceEntity | None:
        result = (await self._session.execute(
            text("""
                WITH RECURSIVE parent_table(id, name, parent_id, ids, cycle) AS (
                SELECT id, name, parent_id, ARRAY[id], false
                FROM spaces WHERE id = :val
                UNION
                    SELECT s.id, s.name, s.parent_id, s.id || p.ids, s.id = ANY(p.ids)
                    FROM spaces as s
                INNER JOIN parent_table p ON p.parent_id = s.id
                WHERE not cycle
                )
                SELECT * FROM parent_table
            """).bindparams(val=id),
        )).fetchall()

        spaces_dict = {elem.id: elem for elem in result}

        return to_three(id, spaces_dict) if result else None


def to_three(space_id: int, models: dict[int, SpaceModel]):
    entities = {
        int(model.id): SpaceEntity(id=model.id, name=model.name)
        for model in models.values()
    }

    for _, v in models.items():

        if v.parent_id not in entities:
            continue

        parent_space = entities.get(v.parent_id)
        if not parent_space:
            raise Exception("Model is empty")

        space = entities.get(v.id)
        if not space:
            raise Exception("Model is not found")

        space.parent = parent_space

    return entities[space_id]
