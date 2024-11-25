import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, lazyload

from app.entities.user import UserEntity
from app.models.user import UserModel
from app.repositories.user import UserRepository
from app.schemas.user import UserRequest
from app.utils.decorators import handle_error
from app.utils.uow import IUnitOfWorkBase, UniqueValueError


class LoginPassUniqueError(Exception):
    pass


class UserService:

    def __init__(self, uow: IUnitOfWorkBase) -> None:
        self._uow = uow

    async def get_members(self):
        async with self._uow as session:
            mems = await session.users.get_all()
            for i in mems:
                print(i)

        return mems
        # async_session = async_sessionmaker(bind=create_async_engine('postgresql+asyncpg://user:pass@localhost:5434/app', echo=True), expire_on_commit=False, )
        # async with async_session() as session:
        #
        #     result = await session.execute(select(UserModel).options(lazyload(UserModel.password)))
        #     models = result.scalars().all()
        #     for i in models:
        #         print(await i.awaitable_attrs.password)
        #
        #     return models

    @handle_error(UniqueValueError, LoginPassUniqueError)
    async def create(self, user: UserRequest) -> UserEntity:
        salt = bcrypt.gensalt(rounds=14)
        hashed_password = bcrypt.hashpw(user.password.encode(), salt)

        async with self._uow as uow:
            member = await uow.users.create(
                email=user.email,
                first_name=user.first_name,
                middle_name=user.middle_name,
                last_name=user.last_name,
                password=hashed_password.decode('utf-8'),
                salt=salt.decode('utf-8')
            )

            await uow.commit()

        return member
