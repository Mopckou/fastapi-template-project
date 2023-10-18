from app.repositories.user import UserRepository
from app.schemas.user import User


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    async def get_users(self):
        return await self._repository.get_all()

    async def create_user(self, user: User):
        return await self._repository.add(
            **user.model_dump()
        )
