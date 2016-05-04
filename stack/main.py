# -*- coding: utf-8 -*-
import sys
import os
from typing import Callable
from stack.args import parser
import stack.config as config
import fabric.main as fabric_main
from fabric.api import local


def new(args):
    local('scaffold new %s %s' % (args.project, args.template))


def upgrade(args):
    local('pip uninstall stack && pip install stack')


def init(args):
    python = args.python or 'python3'
    try:
        local('rm -rf .env')
    except:
        pass
    local('virtualenv .env --python=%s' % python)
    local('.env/bin/pip install ipython coverage flake8 nose')
    projectname = os.path.split(os.path.dirname(os.path.realpath(__name__)))[-1]
    config.write(dict(python=python, project=projectname))


def install(args):
    git = bool(args.install.python) or 'False'
    if not git:
        local('.env/bin/pip install %s' % args.lib)
    if git:
        local('.env/bin/pip install -e git+%s' % args.lib)
    local('.env/bin/pip freeze > requirements.txt')


def uninstall(args):
    return local('.env/bin/pip uninstall %s' % args.lib)


def list_installed(args):
    return local('.env/bin/pip freeze')


def fabric(args):
    return fabric_main.main([os.path.abspath(__file__)])


def coverage(args):
    project = config.load().get('project')
    return local('.env/bin/nosetests -sv --with-coverage --cover-package %s' % project)


def python(args):
    return local('.env/bin/python')


def repl(args):
    return local('.env/bin/ipython')


def pip_exec(args):
    return local('.env/bin/pip')


def git_serve(args):
    port = args.port or '30976'
    ip = args.ip or '0.0.0.0'
    return local('git daemon --reuseaddr --base-path=. --export-all --verbose --enable=receive-pack --port=%s --listen=%s' % (port, ip))


def router(argv) -> Callable:
    args = parser.parse_args()
    if not len(argv) > 1:
        print(parser.format_help())
        return
    return {
        'new': new,
        'repl': repl,
        'pip': pip_exec,
        'python': python,
        'init': init,
        'list': list_installed,
        'uninstall': uninstall,
        'install': install,
        'pass': uninstall,
        'serve': git_serve,
        'coverage': coverage,
    }.get(argv[1], fabric)(args)


def main():
    return router(sys.argv)
