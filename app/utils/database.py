import logging
from abc import ABC, abstractmethod
from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
)

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class IDataBaseMaker(ABC):

    @abstractmethod
    def initial(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()


class PostgresDataBaseMaker(IDataBaseMaker):

    def __init__(self, db_url: str, debug_mode: bool) -> None:
        self.db_url = db_url
        self.debug_mode = debug_mode
        self._engine = None
        self._async_scope_session = None

    def initial(self):
        self._engine = create_async_engine(
            self.db_url,
            echo=self.debug_mode,
        )
        _session_factory = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            expire_on_commit=False,
        )

        self._async_scope_session = async_scoped_session(
            _session_factory,
            scopefunc=current_task,
        )

    async def close(self):
        await self._engine.dispose()

    @property
    def session(self) -> AsyncSession:
        return self._async_scope_session
