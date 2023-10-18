from fastapi import APIRouter

from app.view import user

v1 = APIRouter(
    prefix="/v1",
    tags=["v1"]
)

v1.include_router(user.router)
