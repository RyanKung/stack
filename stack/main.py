# -*- coding: utf-8 -*-
import sys
import os
from typing import Callable
from stack.args import parser
import stack.config as config
import fabric.main as fabric_main


def ignore(fn: Callable, value):
    '''ignore exceptiong'''
    try:
        return fn(value)
    except:
        return None


def new(args):
    os.system('scaffold new %s %s' % (args.project, args.template))


def upgrade(args):
    os.system('pip uninstall stack && pip install stack')


def init(args):
    python = args.python or 'python3'
    ignore(os.system, 'rm -rf .env')
    os.system('virtualenv .env --python=%s' % python)
    os.system('.env/bin/pip install sl_pip')
    os.system('.env/bin/python -m pip install ipython coverage flake8 nose coverage')
    ignore(os.system, '.env/bin/pip install -r ./requirements.txt --process-dependency-links')
    projectname = os.path.split(os.path.dirname(os.path.realpath(__name__)))[-1]
    config.write(dict(python=python, project=projectname))


def setup(args):
    ignore(os.system, '.env/bin/pip install -r ./requirements.txt --process-dependency-links')


def install(args):
    git = bool(args.repo)
    if not git:
        os.system('.env/bin/pip install %s -v --process-dependency-links' % args.lib)
    if git:
        template = config.load().get('git_path', 'git+{repo}#egg={lib}')
        repo = template.format(**dict(repo=args.repo, lib=args.lib))
        os.system('.env/bin/pip install -e %s --process-dependency-links' % repo)
    os.system('.env/bin/pip freeze > requirements.txt')


def uninstall(args):
    return os.system('.env/bin/python -m pip uninstall %s' % args.lib)


def list_installed(args):
    return os.system('.env/bin/pip freeze')


def fabric(args):
    return fabric_main.main([os.path.abspath(__file__)])


def test(args):
    return os.system('.env/bin/nosetests -sv')


def coverage(args):
    project = config.load().get('project')
    return os.system('.env/bin/nosetests -sv --with-coverage --cover-package %s' % project)


def python(args):
    return os.system('.env/bin/python %s' % ' '.join(sys.argv[2:]))


def repl(args):
    return os.system('.env/bin/ipython')


def pip_exec(args):
    return os.system('.env/bin/pip %s' % ' '.join(sys.argv[2:]))


def gen_document(args):
    return os.system('sphinx-apidoc ./ -o ./docs -F')


def git_serve(args):
    port = args.port or '30976'
    ip = args.ip or '0.0.0.0'
    print('git daemon will listen on %s:%s/.git' % (ip, port))
    return os.system('git daemon --reuseaddr --base-path=. --export-all --verbose --enable=receive-pack --port=%s --listen=%s' % (port, ip))


def router(argv) -> Callable:
    args, unknown = parser.parse_known_args()
    if not len(argv) > 1:
        print(parser.format_help())
        return
    return {
        'new': new,
        'repl': repl,
        'test': test,
        'pip': pip_exec,
        'setup': setup,
        'python': python,
        'init': init,
        'list': list_installed,
        'uninstall': uninstall,
        'install': install,
        'pass': uninstall,
        'serve': git_serve,
        'coverage': coverage,
        'doc': gen_document
    }.get(argv[1], fabric)(args)


def main():
    return router(sys.argv)
