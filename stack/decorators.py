# coding utf8
from functools import reduce
from operator import add
from stack.args import subparsers as parser


def command_argument_paraser(fn, parser):

    def doc_parser(doc):
        if not doc:
            return ''
        else:
            kvs = doc.strip().split(', ')
            if kvs[0].startswith('@'):
                return (kvs[0][1:], kvs[1:])
            else:
                return doc

    def add_params(parser, params):
        help_doc = params[1][-1]
        meta_var = params[1][-2]
        parser.add_argument(params[0], *params[1][:2], help=help_doc, metavar=meta_var, type=str)
        return parser

    docs = map(doc_parser, filter(bool, fn.__doc__.split('\n')))
    name = fn.__name__
    params = filter(lambda x: isinstance(x, tuple), docs)
    helps = filter(lambda x: isinstance(x, str), docs)
    command = parser.add_parser(name, help=reduce(add, helps))
    reduce(add_params, params, command)


def command(fn):
    command_argument_paraser(fn, parser)
    return lambda *args, **kwargs: fn(*args, **kwargs)
