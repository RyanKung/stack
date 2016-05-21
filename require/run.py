import runpy
import asyncio
import aiohttp
from .decorators import syncio


loop = asyncio.get_event_loop()


async def fetch(session, url):
    with aiohttp.Timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def run_remote_async(url: str):
    with aiohttp.ClientSession(loop=loop) as session:
        code = await fetch(session, url)
        res = runpy._run_code(code, run_globals=globals())
    return res

run_remote = syncio(run_remote_async)
