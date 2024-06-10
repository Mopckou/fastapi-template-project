from abc import abstractmethod, ABC
from typing import Callable, Optional

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import IRepositoryBase
from app.repositories.user import UserRepository


class NotCreatedSessionError(NotImplementedError):
    ...


class UniqueValueError(Exception):
    ...


ERRORS_MAP = {
    UniqueViolationError: UniqueValueError,
    IntegrityError: UniqueValueError
}


def handle_error(exc_type, exc_value, traceback):
    if exc_type is not None and exc_type in ERRORS_MAP:
        raise ERRORS_MAP[exc_type]


class IUnitOfWorkBase(ABC):
    users: IRepositoryBase

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class PgUnitOfWork(IUnitOfWorkBase):
    users: UserRepository

    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self._session_factory = session_factory
        self._async_session: Optional[AsyncSession] = None

    async def __aenter__(self):
        self._async_session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()

        await self.close()

        handle_error(exc_type, exc_val, exc_tb)

    async def rollback(self):
        await self._async_session.rollback()

    async def close(self):
        await self._async_session.close()

    async def commit(self):
        await self._async_session.commit()

    @property
    def users(self):
        if self._async_session is None:
            raise NotCreatedSessionError()

        return UserRepository(self._async_session)
