# coding utf8
import aiohttp
import asyncio
import sys


class aioInput(object):
    async def __aiter__(self):
        return self

    async def __anext__(self):
        raw = await self.get_input()
        if not raw == 'quit':
            return raw
        else:
            raise StopAsyncIteration

    async def get_input(self):
        await asyncio.sleep(0.5)
        res = input('In ')
        return res


async def ws_client(session, host='ws://127.0.0.1', port='8964'):
    addr = 'ws://{host}:{port}/ws'.format(host=host, port=port)
    async with session.ws_connect(addr) as ws:
        async for raw in aioInput():
            ws.send_str(raw)
            async for msg in ws:
                if msg.tp == aiohttp.MsgType.text:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        print(msg.data)
                        break
                elif msg.tp == aiohttp.MsgType.closed:
                    sys.exit(1)
                elif msg.tp == aiohttp.MsgType.error:
                    sys.exit(0)
    return ws


def main(host='127.0.0.1', port='8964'):
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as client:
        loop.run_until_complete(ws_client(session=client, host=host, port=port))

if __name__ == '__main__':
    main()
