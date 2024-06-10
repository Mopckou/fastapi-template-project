import logging
import traceback

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.schemas.base import BaseResponse
from app.services.user import LoginPassUniqueError


def add_error_handlers(app: FastAPI):
    app.add_exception_handler(Exception, custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError, bad_request_http_exception_handler)
    app.add_exception_handler(LoginPassUniqueError, login_pass_exception_handler)


async def custom_http_exception_handler(request, exc: Exception):
    response = BaseResponse()
    response.errors = [{"message": f"Oops! did something wrong. There goes a rainbow..."}]
    logging.exception(exc)
    print(traceback.format_exc())
    print('exit with err')
    return JSONResponse(
        status_code=500,
        content=response.model_dump(),
    )


async def bad_request_http_exception_handler(request, exc: RequestValidationError):
    response = BaseResponse()
    for e in exc.errors():
        response.errors.append(
            dict(
                message=e['msg'] if "msg" in e else "Unknown msg error...",
                value=e['loc'][1] if "loc" in e else "Unknown location error..."
            )
        )

    return JSONResponse(
        status_code=400,
        content=response.model_dump(),
    )


async def login_pass_exception_handler(request, exc):
    response = BaseResponse()
    response.errors = [{"message": f"Login or password is wrong!"}]
    return JSONResponse(
        status_code=400,
        content=response.model_dump(),
    )


async def authorize_exception_handler(request, exc):
    response = BaseResponse()
    response.errors = [{"message": f"Authorize error!"}]
    return JSONResponse(
        status_code=403,
        content=response.model_dump(),
    )