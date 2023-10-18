from contextlib import AbstractAsyncContextManager
from typing import Callable, Iterator

from sqlalchemy import select, Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_all(self) -> Iterator[Row]:
        async with self.session_factory() as session:
            result = await session.execute(select(User))
            return result.scalars().all()

    async def add(self, email: str, first_name: str, middle_name: str | None, last_name: str | None, **kwargs) -> User:
        async with self.session_factory() as session:
            user = User(email=email, first_name=first_name, middle_name=middle_name, last_name=last_name)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
