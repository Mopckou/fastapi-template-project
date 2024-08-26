from abc import abstractmethod
from typing import Union, Iterator
from uuid import UUID

from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.project import ProjectEntity
from app.models.project import ProjectModel
from app.repositories.base import BaseRepository, IRepositoryBase


class IProjectRepository(IRepositoryBase):

    @abstractmethod
    async def create(self, *args, **kwargs) -> ProjectEntity:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_member(self, id: Union[int, UUID]) -> Iterator[Row]:
        raise NotImplementedError()


class ProjectRepository(BaseRepository, IProjectRepository):
    __table_cls__ = ProjectModel
    __entity_model__ = ProjectEntity

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, name: str, main_branch: str, vcs_url: str, deploy_system_url: str) -> ProjectEntity:
        project = ProjectModel(
            name=name,
            main_branch=main_branch,
            vcs_url=vcs_url,
            deploy_system_url=deploy_system_url
        )

        self._session.add(project)
        await self._session.flush()

        return ProjectEntity(**vars(project))

    async def get_by_member(self, member_id: UUID) -> list[ProjectEntity]:


        return ProjectEntity(**vars(service))



    async def get_by_id(self, id: Union[int, UUID]) -> Iterator[SpaceEntity]:
        parent_alias = aliased(SpaceModel)
        # result = (await self._session.scalars(
        #     select(SpaceModel).options(
        #         joinedload(SpaceModel.children),
        #         joinedload(SpaceModel.parent)
        #     ).where(SpaceModel.id == id).join(SpaceModel.parent.of_type(parent_alias), full=True)
        # )).unique().all()

        result = (await self._session.scalars(
            select(SpaceModel).options(
                #selectinload(SpaceModel.children, recursion_depth=2),
                selectinload(SpaceModel.parent, recursion_depth=2), # проверить как работает глубина рекурсии
                # joinedload(SpaceModel.projects_associations),
                # joinedload(SpaceModel.projects)
            ).where(SpaceModel.id == id).join(SpaceModel.parent.of_type(parent_alias), full=True)
        )).unique().all()

        return [SpaceEntity(**vars(model)) for model in result]

    # async def get_by_id(self, id: Union[int, UUID]) -> list:
    #     parent_alias = aliased(SpaceModel, name='s')
    #
    #     # result = (await self._session.scalars(
    #     #     select(SpaceModel).options(
    #     #         selectinload(SpaceModel.children, recursion_depth=1),
    #     #         selectinload(SpaceModel.parent, recursion_depth=1),
    #     #         joinedload(SpaceModel.projects_associations),
    #     #         joinedload(SpaceModel.projects)
    #     #     ).where(SpaceModel.id == id).join(SpaceModel.parent.of_type(parent_alias), full=True)
    #     #
    #     # )).unique().all()
    #
    #     parent_table = select(SpaceModel).where(SpaceModel.id == 3).cte("parent_table", recursive=True)
    #     parent_table_alias = aliased(SpaceModel, parent_table, name='p')
    #     q = parent_table.union(
    #         select(parent_alias).join(
    #             parent_table, parent_table.c.id == parent_alias.parent_id
    #         )
    #     )
    #     r = aliased(SpaceModel, alias=q)  # этот элиас позволяет вывести объекты в результате
    #     result = (await self._session.scalars(
    #         select(r)
    #     )).unique().all()
    #     print(result)
    #     print(result[0])
    #
    #     return [SpaceEntity(**vars(model)) for model in result]