from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.services.space import SpaceService
from app.containers import Container
from app.schemas.space import SpaceResponse

router = APIRouter(
    tags=["spaces"],
)


@router.get("/spaces/{space_id}", response_model=SpaceResponse)
@inject
async def create_space(
    space_id: int, space_service: SpaceService = Depends(Provide[Container.services.space])
):
    space = await space_service.get_three_by_id(space_id)
    return {"result": space}
