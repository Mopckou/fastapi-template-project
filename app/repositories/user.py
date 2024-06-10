from abc import abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.user import UserEntity
from app.models.user import UserModel, PasswordModel
from app.repositories.base import BaseRepository, IRepositoryBase


class IUserRepository(IRepositoryBase):

    @abstractmethod
    async def create(self, *args, **kwargs) -> UserEntity:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_login(self, login: str) -> UserEntity:
        raise NotImplementedError()


class UserRepository(BaseRepository, IUserRepository):
    __table_cls__ = UserModel
    __entity_model__ = UserEntity

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(
        self,
        email: str,
        first_name: str,
        middle_name: str | None,
        last_name: str | None,
        password: str,
        salt: str,
        **kwargs
    ) -> UserEntity:
        member = UserModel(email=email, first_name=first_name, middle_name=middle_name, last_name=last_name)
        member.password = PasswordModel(hash=password, salt=salt)
        self._session.add(member)
        await self._session.flush()

        return UserEntity(**vars(member))

    async def get_by_login(self, login: str) -> UserEntity | None:
        result = await self._session.execute(select(UserModel).where(UserModel.email == login))
        member = result.scalars().one_or_none()

        return UserEntity(**vars(member)) if member is not None else None
