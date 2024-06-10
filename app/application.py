from fastapi import FastAPI

from app.containers import Container
from app import middlewares
from app.middlewares import CustomRequestMiddleware
from app.routes import v1
from app.view import tech, user
from app.utils.exception_handlers import add_error_handlers


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[middlewares, user])
    app = FastAPI(
        title="ExampleApi",
        description="Backend for awesome service.",
        version="0.0.1",
        license_info={
            "name": "Apache 2.0",
            "identifier": "MIT",
        },
        lifespan=middlewares.lifespan,
    )
    app.container = container
    app.add_middleware(
        CustomRequestMiddleware
    )
    add_error_handlers(app)

    app.include_router(tech.router)
    app.include_router(v1)
    return app
