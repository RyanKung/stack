# -*- coding: utf-8 -*-
import sys
import os
from typing import Callable
from stack.args import parser
import stack.config as config
import stack.util as util
from stack.decorators import as_command
import sysconfig
import traceback

config_file_exist = config.exist()
current_path = os.path.dirname(os.path.abspath(__file__))


def ignore(fn: Callable, value):
    '''ignore exceptiong'''
    try:
        return fn(value)
    except:
        return None


@as_command
def new(args):
    '''
    Initalize a new project based on template
    @argument project, metavar=PROJECT, help=your project name
    @argument -t, --template, metavar=template, help=External template path, default=default
    '''
    if args.template == 'default':
        args.template = '%s/../templates/default' % current_path
    import scaffold.main
    return scaffold.main.main(args=args)


@as_command
def upgrade(args):
    '''
    Upgrade Stack
    '''
    os.system('pip uninstall stack && pip install stack')


@as_command
def clear(args):
    '''
    Remove virtualenv
    '''
    ignore(os.system, 'rm -rf .env')


@as_command
def init(args):
    '''
    Initalize a new project envirement
    @argument --python, metavar=PATH, help=Version of Python, default=python3
    '''
    python = args.python or 'python3'
    config.write(dict(python=python))
    config.write(dict(python_exec='.env/bin/python'))
    os.system('virtualenv .env --python=%s' % python)
    os.system('.env/bin/pip install sl_pip')
    os.system('.env/bin/pip install ipython coverage flake8 nose coverage')
    if python == 'python3':
        util.info('Installing stack inside venv')
        os.system('.env/bin/pip install python_stack')


@as_command
def setup(args):
    '''
    Install libs from requirements.txt to venv
    '''
    ignore(os.system, '.env/bin/pip install -r ./requirements.txt --process-dependency-links')
    projectname = os.path.split(os.path.dirname(os.path.realpath(__name__)))[-1]
    config.write(dict(project=projectname))


@as_command
def install(args):
    '''
    Install libs from pypi or git repos
    @argument lib, metavar=LIB, help=Lib name
    @argument --repo, metavar=repo, help=Install via a git repo
    @argument --git, metavar=git, help=Decare is a git repo, default=
    '''
    if not args.lib:
        ignore(os.system, '.env/bin/pip install -r ./requirements.txt --process-dependency-links')
    git = bool(args.repo)
    if not git:
        os.system('.env/bin/pip install %s -v --process-dependency-links' % args.lib)
    if git:
        template = config.load().get('git_path', 'git+{repo}#egg={lib}')
        repo = template.format(**dict(repo=args.repo, lib=args.lib))
        os.system('.env/bin/pip install -e %s --process-dependency-links' % repo)
    os.system('.env/bin/pip freeze > requirements.txt')


@as_command
def uninstall(args):
    '''
    Uninstall libs
    @argument lib, metavar=LIB, help=Lib name
    '''
    return os.system('.env/bin/pip uninstall %s' % args.lib)


@as_command
def installed(args):
    '''
    List installed libs
    '''
    import pip
    list(map(print, pip.commands.freeze.freeze()))


@as_command
def fabric(args):
    '''
    drop to Fabric
    '''
    import fabric.main
    return fabric.main.main([os.path.abspath(__file__)])


@as_command
def test(args):
    '''
    run unittest
    '''
    return os.system('.env/bin/nosetests -sv')


@as_command
def coverage(args):
    '''
    Report unittest coverage
    '''
    project = config.load().get('project')
    return os.system('.env/bin/nosetests -sv --with-coverage --cover-package %s' % project)


@as_command
def python(args):
    '''
    run python
    '''
    return os.system('.env/bin/python %s' % ' '.join(sys.argv[2:]))


@as_command
def repl(args):
    '''
    call ipython as repl
    '''
    return os.system('.env/bin/ipython')


@as_command
def pip(args):
    '''
    call pip
    '''
    return os.system('.env/bin/pip %s' % ' '.join(sys.argv[2:]))


@as_command
def doc(args):
    '''
    audto gen document
    '''
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
        'pip': pip,
        'setup': setup,
        'python': python,
        'init': init,
        'clear': clear,
        'installed': installed,
        'uninstall': uninstall,
        'install': install,
        'pass': uninstall,
        'serve': git_serve,
        'coverage': coverage,
        'doc': doc
    }.get(argv[1], fabric)(args)


def main():
    if len(sys.argv) > 1 and not util.is_venv() and not sys.argv[1] == 'init':
        util.warn('Warning: Command running outside the venv, you may need to run `stack init` first')
        util.warn('Warning: Using lib path %s' % sysconfig.get_path('platlib'))
        if config.has_venv() and config.load().get('python', '') == 'python3':
            util.info('Try switching to .env/bin/python')
            os.system('.env/bin/stack %s' % ''.join(sys.argv[1:]))
    else:
        try:
            router(sys.argv)
        except Exception as ex:
            util.error("Exception <%s>, Traceback: %r", str(ex), traceback.format_exc())

if __name__ == '__main__':
    main()
