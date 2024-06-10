from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.containers import Container
from app.schemas.user import NewUserResponse, UserRequest, UsersResponse
from app.services.user import UserService

router = APIRouter(
    tags=["users"],
)


@router.get("/users", response_model=UsersResponse)
@inject
async def get_users(user_service: UserService = Depends(Provide[Container.services.user])):
    users = await user_service.get_members()

    return {"result": users}


@router.post("/users", response_model=NewUserResponse)
@inject
async def create_user(request_model: UserRequest, user_service: UserService = Depends(Provide[Container.services.user])):
    new_user = await user_service.create(request_model)

    return {"result": new_user}
