# -*- coding: utf-8 -*-
import sys
import re
import os
from typing import Callable
from stack.args import parser


def new(args):
    from stack.scaffold.template import render
    template_params = dict(project=args.project, __project__=args.project)
    return list(render(args.template, template_params))


def install(args):
    pass


def uninstall(args):
    pass


def fab_main(args):
    from fabric.main import main as fab_main
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    return lambda x: fab_main([os.path.abspath(__file__)])


def router(argv) -> Callable:
    return {
        'new': new,
        'install': install,
        'pass': uninstall
    }.get(argv['1'], fab_main)


def main(argv, kwargs):
    return router(argv[1])(kwargs)

sys.exit(main(sys.argv, parser.parse_args()))
# sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
# sys.exit(main([os.path.abspath(__file__)]))
