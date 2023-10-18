import logging
from asyncio import current_task
from contextlib import AbstractContextManager, asynccontextmanager
from typing import Callable

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
)

logger = logging.getLogger(__name__)

Base = declarative_base()


class DataBase:

    def __init__(self, db_url: str, debug_mode: bool) -> None:
        self.db_url = db_url
        self.debug_mode = debug_mode
        self._engine = None
        self._async_scope_session = None

    def init_db(self):
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

    async def close_connections(self):
        await self._engine.dispose()

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        async_session: AsyncSession = self._async_scope_session()
        try:
            yield async_session
        except Exception:
            logger.exception("Session rollback because of exception")
            await async_session.rollback()
            raise
        finally:
            await async_session.close()
