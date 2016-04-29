# -*- coding: utf-8 -*-
import sys
import os
from typing import Callable
from stack.args import parser
import virtualenv
import pip
import scaffold.main as scaffold_main
import fabric.main as fabric_main


def new(args):
    return scaffold_main.main()


def init(args):
    sys.argv[1] = '.env'
    return virtualenv.main()


def install(args):
    return pip.main()


def uninstall(args):
    return pip.main()


def list_installed(args):
    list(map(print, pip.commands.freeze.freeze()))


def fabric(args):
    return fabric_main.main([os.path.abspath(__file__)])


def router(argv) -> Callable:
    args = parser.parse_args()
    if not len(argv) > 1:
        print(parser.format_help())
        return
    return {
        'new': new,
        'init': init,
        'list': list_installed,
        'install': install,
        'pass': uninstall
    }.get(argv[1], fabric)(args)


def main():
    return router(sys.argv)
