from contextlib import asynccontextmanager

from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends
from starlette.types import ASGIApp, Scope, Receive, Send

from app.containers import Container
from app.database import DataBase
from app.repositories.user import UserRepository


@asynccontextmanager
@inject
async def lifespan(app: FastAPI, db: DataBase = Depends(Provide[Container.db])):
    db.init_db()
    yield
    await db.close_connections()


class CustomRequestMiddleware:
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    @inject
    async def __call__(self, scope: Scope, receive: Receive, send: Send, user: UserRepository = Depends(Provide[Container.user_repository])) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        print(await user.get_all())
        await self.app(scope, receive, send)
