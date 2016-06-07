# -*- coding: utf-8 -*-
import sys
import os
from typing import Callable
from stack import parser, as_command
import stack.utils as util
from stack.main import main as cli_main
from stack.decorators import ignore
import sysconfig
import traceback


__all__ = ['new', 'upgrade', 'clear',
           'setup', 'install', 'uninstall', 'fab', 'test',
           'coverage', 'run', 'python', 'repl', 'doc',
           'serve', 'pep8_hook', 'pip']

current_path = os.path.dirname(os.path.abspath(__file__))
prefix = util.get_env()


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
def setup(args) -> None:
    '''
    Install libs from requirements.txt to venv
    @argument -r, --requirefile, default='requirement.txt', help=sepec requirement file
    '''
    ignore(os.system, prefix + 'pip install -r ./requirements.txt --process-dependency-links')


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
        return os.system(prefix + 'python %s' % ' '.join(sys.argv[2:]))


@as_command
def python(args) -> None:
    '''
    Run python
    '''
    return os.system(prefix + 'python %s' % ' '.join(sys.argv[2:]))


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
    util.info('Using %spython' % prefix)
    if not prefix:
        util.warn('Command running outside the venv, you may need to activite your `venv` first')
        util.warn('Using lib path %s' % sysconfig.get_path('platlib'))
        util.info('Continue? (Y/n)')
        if input().upper() == 'N':
            sys.exit()
    try:
        cli_main(argv=sys.argv, pattern=pattern, allow=('stackfile', 'execfile'))
    except Exception as ex:
        util.error("Exception <%s>, Traceback:" % str(ex))
        util.error(traceback.format_exc())

if __name__ == '__main__':
    if sys.version_info[:2] < (3, 5) and sys.argv[-1] == 'install':
        sys.exit('stack requires python 3.5 or higher')
    main()
