from abc import abstractmethod
from typing import Union, Iterator
from uuid import UUID

from sqlalchemy import Row, select, bindparam, text, column, literal
from sqlalchemy.dialects.postgresql import array
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

    async def get_by_id(self, id: int) -> SpaceEntity | None:
        """
        Чистый sql запрос:
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
        :param space_id:
        :return:
        """

        parent_table = (
            select(SpaceModel.id, SpaceModel.name, SpaceModel.parent_id, SpaceModel.created_at, SpaceModel.updated_at, (array([column("id")])).label("ids"), literal(False).label('cycle'))
            .where(SpaceModel.id == id)
            .cte("parent_table", recursive=True)
        )
        children_alias = aliased(SpaceModel, name='s')

        q = parent_table.union(
            select(
                children_alias.id,
                children_alias.name,
                children_alias.parent_id,
                children_alias.created_at,
                children_alias.updated_at,
                (column('ids').op('||')(children_alias.id)).label("ids"),
                parent_table.c.ids.any(children_alias.id).label("cycle")
            )
            .join(parent_table, parent_table.c.parent_id == children_alias.id)
            .where(parent_table.c.cycle == False)
        )

        result = (await self._session.scalars(
            select(aliased(SpaceModel, alias=q))
        )).unique().fetchall()

        return self.map_to_entity(
            result[0] if result else None
        )  # noqa

    def map_to_entity(self, model: SpaceModel | None) -> SpaceEntity | None:
        if not model:
            return None

        return SpaceEntity(
            id=model.id,
            name=model.name,
            parent=self.map_to_entity(model.parent)
        )
