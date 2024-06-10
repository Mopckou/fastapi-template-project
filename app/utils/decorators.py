import functools
from typing import Type


def handle_error(catch_error: Type[Exception], raise_error: Type[Exception]):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except catch_error:
                raise raise_error
        return wrapped
    return wrapper
