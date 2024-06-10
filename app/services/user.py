import bcrypt

from app.entities.user import UserEntity
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
            return await session.users.get_all()

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
