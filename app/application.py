from fastapi import FastAPI

from app.containers import Container
from app import middlewares
from app.middlewares import CustomRequestMiddleware
from app.routes import v1
from app.view import tech, user


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[middlewares, tech, user])

    app = FastAPI(lifespan=middlewares.lifespan)
    app.container = container
    app.add_middleware(
        CustomRequestMiddleware
    )
    app.include_router(tech.router)
    app.include_router(v1)

    return app
