# -*- coding: utf-8 -*-
import sys
import os
from typing import Callable
from stack.args import parser
from fabric.main import main as fab_main
from pip import main as pip_main


def new(args):
    from stack.scaffold.template import render
    template_params = dict(project=args.project, __project__=args.project)
    return list(render(args.template, template_params))


def install(args):
    return pip_main()


def uninstall(args):
    return pip_main()


def fabric_main(args):
    return fab_main([os.path.abspath(__file__)])


def router(argv) -> Callable:
    return {
        'new': new,
        'install': install,
        'pass': uninstall
    }.get(argv[1], fabric_main)


def main():
    return router(sys.argv)(parser.parse_args())
