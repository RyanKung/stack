# coding utf8


from aiohttp import web
from typing import Callable
from functools import partial


def command_parser(cmd: str, fns: dict) -> Callable:
    '''
    get target function from funs dict and \
    map command like "cmd arg0 arg1 arg2 --key1=v1 --key2=v2" to \
    partial(fn, arg0, arg1, arg2, key1=v1, key2=v2)
    '''
    args = cmd.strip().split(' ')
    fn_name = args[0]
    args = [i for i in args[1:] if not i.startswith('-')]
    kwargs = dict([i.replace('-', '').split('=') for i in args[1:] if i.startswith('-')])
    return partial(fns.get(fn_name, None), *args, **kwargs)


async def wsh(request, handler=print):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.tp == web.MsgType.text:
            handler(msg.data)
            ws.send_str("Hello, {}".format(msg.data))
        elif msg.tp == web.MsgType.binary:
            ws.send_bytes(msg.data)
        elif msg.tp == web.MsgType.close:
            print('websocket connection closed')
    return ws


def main(host='127.0.0.1', port='8964'):
    app = web.Application()
    app.router.add_route('GET', '/ws', wsh)
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
