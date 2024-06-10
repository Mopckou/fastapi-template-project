from contextlib import asynccontextmanager

from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends
from starlette.types import ASGIApp, Scope, Receive, Send

from app.containers import Container
from app.database import PostgresDataBaseMaker
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.utils.uow import PgUnitOfWork


@asynccontextmanager
@inject
async def lifespan(_: FastAPI, db: PostgresDataBaseMaker = Depends(Provide[Container.gateways.db])):
    db.initial()
    yield
    await db.close()


class CustomRequestMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    @inject
    async def __call__(self, scope: Scope, receive: Receive, send: Send, users: UserService = Depends(Provide[Container.services.user])) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        print(await users.get_members())
        await self.app(scope, receive, send)
