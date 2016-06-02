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


__all__ = ['new', 'upgrade', 'clear', 'set_python', 'init',
           'setup', 'install', 'uninstall', 'fab', 'test',
           'coverage', 'run', 'python', 'repl', 'doc',
           'serve', 'pep8_hook', 'pip']

config_file_exist = config.exist()
current_path = os.path.dirname(os.path.abspath(__file__))
prefix = config.get_prefix()


def ignore(fn: Callable, value):
    '''ignore exceptiong'''
    try:
        return fn(value)
    except:
        return None


@as_command
def new(args) -> None:
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
def upgrade(args) -> None:
    '''
    Upgrade Stack
    '''
    os.system('pip uninstall stack && pip install stack')


@as_command
def clear(args) -> None:
    '''
    Remove virtualenv
    '''
    ignore(os.system, 'rm -rf .env')


@as_command
def set_python(args) -> None:
    '''
    Set python version
    @argument --python, metavar=version, help=Version of Python
    '''
    config.write(dict(python=python))


@as_command
def init(args) -> None:
    '''
    Initalize a new project envirement
    @argument --python, metavar=PATH, help=Version of Python, default=python3
    @argument --install_all, metavar=all, help=Install all required lib
    '''
    python = args.python or 'python3'
    config.write(dict(python=python))
    config.write(dict(python_exec=prefix + 'python'))
    os.system('virtualenv .env --python=%s' % python)
    if args.install_all:
        os.system(prefix + 'pip install ipython coverage flake8 nose coverage')


@as_command
def setup(args) -> None:
    '''
    Install libs from requirements.txt to venv
    @argument -r, --requirefile, default='requirement.txt', help=sepec requirement file
    '''
    dependence = map(lambda x: x.split('==')[0], tuple(open('requirements.txt')))
    ignore(os.system, prefix + 'pip install -r ./requirements.txt --process-dependency-links')
    projectname = os.path.split(os.path.dirname(os.path.realpath(__name__)))[-1]
    config.write(dict(project=projectname))
    config.write(dict(dependence=dependence))


@as_command
def install(args) -> None:
    '''
    Install libs from pypi or git repos
    @argument lib, metavar=LIB, help=Lib name
    @argument --repo, metavar=repo, help=Install via a git repo
    '''
    if not args.lib:
        ignore(os.system, prefix + 'pip install -r ./requirements.txt --process-dependency-links')
    git = bool(args.repo)
    if not git:
        os.system(prefix + 'pip install %s -v --process-dependency-links' % args.lib)
    if git:
        template = 'git+{repo}#egg={lib}'
        repo = template.format(**dict(repo=args.repo, lib=args.lib))
        os.system(prefix + 'pip install -e %s --process-dependency-links' % repo)
    os.system(prefix + 'pip freeze > requirements.txt')


@as_command
def uninstall(args) -> None:
    '''
    Uninstall libs
    @argument lib, metavar=LIB, help=Lib name
    '''
    util.check_exec('pip')
    return os.system(prefix + 'pip uninstall %s' % args.lib)


@as_command
def installed(args) -> None:
    '''
    List installed libs
    '''
    if util.is_venv():
        import pip
        list(map(print, pip.commands.freeze.freeze()))
    else:
        util.check_exec('pip')
        os.system(prefix + 'pip freeze')


@as_command
def fab(args) -> None:
    '''
    Drop to Fabric
    '''
    os.system(prefix + 'fab %s' % ' '.join(sys.argv[2:]))


@as_command
def pip(args) -> None:
    '''
    Run to pip
    '''
    os.system(prefix + 'pip %s' % ' '.join(sys.argv[2:]))


@as_command
def test(args) -> None:
    '''
    Run unittest with nosetests
    '''
    return os.system(prefix + 'nosetests -sv')


@as_command
def coverage(args) -> None:
    '''
    Report unittest coverage
    '''
    util.check_exec('nosetests')
    project = os.path.split(os.path.dirname(os.path.realpath(__name__)))[-1]
    return os.system(prefix + 'nosetests -sv --with-coverage --cover-package %s' % project)


@as_command
def run(args) -> None:
    '''
    Exec file locally or remote
    @argument --remote, metavar=remote, help=run as remote file
    '''
    if args.remote:
        return os.system('require run %s' % args.remote)
    else:
        python = config.load().get('python', 'python')
        return os.system(prefix + '%s %s' % (python, ' '.join(sys.argv[2:])))


@as_command
def python(args) -> None:
    '''
    Run python
    '''
    python = config.load().get('python', 'python')
    return os.system(prefix + '%s %s' % (python, ' '.join(sys.argv[2:])))


@as_command
def repl(args) -> None:
    '''
    Call ipython as repl
    '''
    util.check_exec('ipython')
    return os.system(prefix + 'ipython' % ' '.join(sys.argv[2:]))


@as_command
def doc(args) -> None:
    '''
    Auto gen document
    '''
    util.check_exec('sphinx')
    return os.system('sphinx-apidoc ./ -o ./docs -f -M -F')


@as_command
def serve(args) -> None:
    '''
    Serve current dir as as git daemon
    @argument --ip, help=IP addr
    @argument --port, help=Port
    '''
    port = args.port or '30976'
    ip = args.ip or '0.0.0.0'
    print('git daemon will listen on %s:%s/.git' % (ip, port))
    return os.system('git daemon --reuseaddr --base-path=. --export-all --verbose --enable=receive-pack --port=%s --listen=%s' % (port, ip))


@as_command
def pep8_hook(args) -> None:
    '''
    Add a pre commit hook to your .git repo
    '''
    os.system('flake8 --install-hook')


def router(pattern: dict, argv) -> Callable:
    args, unknown = parser.parse_known_args()
    if not len(argv) > 1:
        print(parser.format_help())
        return
    return pattern.get(argv[1], fab)(args)


def main():
    pattern = {k: v for k, v in globals().items() if k in __all__}
    util.check_and_update_via_stackfile(pattern)
    util.check_and_update_via_execsfile(pattern, prefix)
    util.info('Using %spython' % (prefix or (util.is_venv() and 'Venv') or 'System Default '))
    if len(sys.argv) > 1 and not config.has_venv() and not sys.argv[1] == 'init' and not util.is_venv():
        util.warn('Command running outside the venv, you may need to run `stack init` first, or activite your `venv`')
        util.warn('Using lib path %s' % sysconfig.get_path('platlib'))
        util.info('Continue? (Y/n)')
        if input().upper() == 'N':
            sys.exit()
    try:
        router(pattern, sys.argv)
    except Exception as ex:
        util.error("Exception <%s>, Traceback:" % str(ex))
        util.error(traceback.format_exc())

if __name__ == '__main__':
    if sys.version_info[:2] < (3, 5) and sys.argv[-1] == 'install':
        sys.exit('stack requires python 3.5 or higher')
    main()
