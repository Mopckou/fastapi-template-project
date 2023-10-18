from typing import Annotated

from fastapi import APIRouter, Depends

from app.settings import Settings, get_settings

router = APIRouter(
    tags=["tech"]
)


@router.get("/")
async def hello():
    return {"message": "Hello World"}


@router.get("/ping")
async def ping():
    return {"message": "OK"}


@router.get("/mode")
async def mode(settings: Annotated[Settings, Depends(get_settings)]):
    return {"debug_mode": settings.debug}
