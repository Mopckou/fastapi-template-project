from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query

from app.services.space import SpaceService
from app.containers import Container
from app.schemas.space import SpaceResponse

router = APIRouter(
    tags=["spaces"],
)


@router.get("/spaces/{space_id}", response_model=SpaceResponse)
@inject
async def get_spaces(
    space_id: int, space_service: SpaceService = Depends(Provide[Container.services.space])
):
    space = await space_service.get_three_by_id(space_id)
    return {"result": space}


@router.post("/spaces/{space_id}/generate", response_model=SpaceResponse)
@inject
async def generate_spaces(
    space_id: int,
    depth: Annotated[tuple[int] | None, Query()] = None,
    space_service: SpaceService = Depends(Provide[Container.services.space])
):
    space = await space_service.generate_spaces(space_id, depth)
    return {"result": space}
