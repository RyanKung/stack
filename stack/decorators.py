# coding utf8
from functools import reduce, wraps
from operator import add
from stack.args import subparsers as parser
from typing import Callable


def command_argument_paraser(fn: Callable, parser) -> list:

    def doc_parser(doc: str) -> str:
        if not doc:
            return ''
        else:
            kvs = doc.strip().split(', ')
            if kvs[0].startswith(('@', ':')):
                return [kvs[0].split(' ')[1]] + kvs[1:]
            else:
                return doc.strip()

    def add_params(parser, param: list):
        argc = (p for p in param if '=' not in p)
        kwargs = dict((tuple(p.split('=')) for p in param if '=' in p))
        parser.add_argument(*argc, **kwargs, type=str)
        return parser

    docs = map(doc_parser, filter(bool, fn.__doc__.split('\n')))
    name = fn.__name__
    params = filter(lambda x: isinstance(x, list), docs)
    helps = filter(lambda x: isinstance(x, str), docs)
    command = parser.add_parser(name, help=reduce(add, helps))
    return reduce(add_params, params, command)


def as_command(fn):
    command_argument_paraser(fn, parser)

    @wraps(fn)
    def handler(*args, **kwargs):
        return fn(*args, **kwargs)

    return handler


def ignore(fn):
    @wraps(fn)
    def hander(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except:
            None
