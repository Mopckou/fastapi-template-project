from cffi.backend_ctypes import xrange
from faker import Faker

from app.entities.space import SpaceEntity
from app.utils.uow import IUnitOfWorkBase


class SpaceService:

    def __init__(self, uow: IUnitOfWorkBase) -> None:
        self._uow = uow

    async def get_three_by_id(self, space_id: int) -> SpaceEntity:
        async with self._uow as uow:
            space = await uow.spaces.get_by_id(
                id=space_id
            )

        return space

    async def generate_spaces(self, space_id: int, depth: tuple[int] | None) -> SpaceEntity:
        async with self._uow as uow:
            fake = Faker()

            if not depth:
                new = await uow.spaces.create(
                    name=fake.word() + " " + str(fake.random_digit()),
                    parent_space_id=space_id
                )
                await uow.commit()
                return new

            parent_space_id = space_id
            for value in xrange(1, depth[0] + 1):
                name = fake.word() + " " + str(fake.random_digit())
                new_space = await uow.spaces.create(
                    name=name,
                    parent_space_id=parent_space_id
                )
                _ = await uow.spaces.create(
                    name="left " + name,
                    parent_space_id=parent_space_id
                )
                _ = await uow.spaces.create(
                    name="right " + name,
                    parent_space_id=parent_space_id
                )
                parent_space_id = new_space.id

            await uow.commit()

        return new_space
