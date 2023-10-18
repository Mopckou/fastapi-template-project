from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.containers import Container
from app.schemas.user import User
from app.services.user import UserService

router = APIRouter(
    tags=["users"]
)


@router.get("/users")
@inject
async def get_users(user: UserService = Depends(Provide[Container.user_service])):
    return {"users": await user.get_users()}


@router.post("/user/create")
@inject
async def create_user(user: User, user_service: UserService = Depends(Provide[Container.user_service])):
    new_user = await user_service.create_user(user)

    return {"id": new_user.id}
