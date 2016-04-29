# -*- coding: utf-8 -*-
import sys
import os
from typing import Callable
from stack.args import parser
import fabric
import scaffold
import virtualenv
import pip


def new(args):
    return scaffold.main()


def init(args):
    sys.argv[1] = '.env'
    return virtualenv.main()


def install(args):
    return pip.main()


def uninstall(args):
    return pip.main()


def list_installed(args):
    list(map(print, pip.commands.freeze.freeze()))


def fabric_main(args):
    return fabric.main.main([os.path.abspath(__file__)])


def router(argv) -> Callable:
    return {
        'new': new,
        'init': init,
        'list': list_installed,
        'install': install,
        'pass': uninstall
    }.get(argv[1], fabric_main)


def main():
    return router(sys.argv)(parser.parse_args())
