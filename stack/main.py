# -*- coding: utf-8 -*-
import sys
import os
from typing import Callable
from stack.args import parser
from fabric.main import main as fab_main
from scaffold.main import main as scaffold_main
from pip import main as pip_main


def new(args):
    return scaffold_main()


def pip_install(args):
    return pip_main()


def pip_uninstall(args):
    return pip_main()


def pip_list(args):
    sys.argv[1] = 'freeze'
    return pip_main()


def fabric_main(args):
    return fab_main([os.path.abspath(__file__)])


def router(argv) -> Callable:
    return {
        'new': new,
        'list': pip_list,
        'install': pip_install,
        'pass': pip_uninstall
    }.get(argv[1], fabric_main)


def main():
    return router(sys.argv)(parser.parse_args())
