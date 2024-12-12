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
