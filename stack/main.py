# -*- coding: utf-8 -*-
import sys
import os
from typing import Callable
from stack.args import parser
from fabric.main import main as fab_main
from scaffold.main import main as scaffold_main
from virtualenv import main as virtualenv_main
from pip import main as pip_main


def new(args):
    return scaffold_main()


def init(args):
    sys.argv[1] = '.env'
    return virtualenv_main()


def install(args):
    return pip_main()


def uninstall(args):
    return pip_main()


def list_installed(args):
    sys.argv[1] = 'freeze'
    return pip_main()


def fabric_main(args):
    return fab_main([os.path.abspath(__file__)])


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
