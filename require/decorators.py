# coding:utf8

from functools import wraps, partial
import asyncio

loop = asyncio.get_event_loop()


def syncio(fn, loop):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return loop.run_until_complete(fn(*args, **kwargs))
    return wrapper

syncio = partial(syncio, loop=loop)
