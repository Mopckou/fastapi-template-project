from app.entities.space import SpaceEntity
from app.utils.uow import IUnitOfWorkBase


class SpaceService:

    def __init__(self, uow: IUnitOfWorkBase) -> None:
        self._uow = uow

    async def get_three_by_id(self, space_id: int) -> SpaceEntity:
        async with self._uow as uow:
            space = await uow.spaces.get_by_id(
                space_id=space_id
            )

        return space

