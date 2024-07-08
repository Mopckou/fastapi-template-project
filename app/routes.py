from fastapi import APIRouter

from app.view import user, space

v1 = APIRouter(
    prefix="/v1",
    tags=["v1"]
)

v1.include_router(user.router)
v1.include_router(space.router)
