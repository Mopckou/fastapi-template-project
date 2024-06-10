from abc import abstractmethod, ABC
from typing import Iterator, Union, Type, Sequence
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, delete, Row
from sqlalchemy.ext.asyncio import AsyncSession


class IRepositoryBase(ABC):

    @abstractmethod
    async def get_all(self) -> Iterator[Row]:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, id: Union[int, UUID]) -> Iterator[Row]:
        raise NotImplementedError()

    @abstractmethod
    async def delete_by_id(self, id: Union[int, UUID]) -> None:
        raise NotImplementedError()


class BaseRepository(IRepositoryBase):

    __table_cls__ = ...
    __entity_model__: Type[BaseModel] = ...

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> Sequence[BaseModel]:
        result = await self._session.execute(select(self.__table_cls__))
        models = result.scalars().all()

        return [self.__entity_model__(**vars(model)) for model in models]

    async def get_by_id(self, id: Union[int, UUID]) -> BaseModel:
        result = await self._session.execute(select(self.__table_cls__).where(self.__table_cls__.id == id))
        model = result.scalars().one()

        return self.__entity_model__(**vars(model))

    async def delete_by_id(self, id: Union[int, UUID]) -> None:
        await self._session.execute(delete(self.__table_cls__).where(self.__table_cls__.id == id))
