# -*- coding: utf-8 -*-
import sys
import os
from functools import partial
from typing import Callable
from stack import parser, as_command, pattern
import stack.utils as util
from stack.main import main as cli_main
from stack.decorators import ignore
import traceback
import subprocess


__all__ = ['new', 'upgrade', 'clear',
           'setup', 'install', 'uninstall', 'fab', 'test',
           'coverage', 'run', 'python', 'repl', 'doc',
           'serve', 'pep8_hook', 'pip', 'stop_serve']

current_path = os.path.dirname(os.path.abspath(__file__))
prefix = util.get_env()


def local(cmd, block=True):
    res = partial(subprocess.Popen, shell=True,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.PIPE,
                  stdin=subprocess.PIPE)(cmd)
    if block:
        out = res.stdout.readline().decode()
        err = res.stderr.readline().decode()
        out and util.info(out)
        err and util.error(err)
        return res
    return res


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
    local('pip uninstall stack && pip install stack')


@as_command
def clear(args) -> None:
    '''
    Remove virtualenv
    '''
    ignore(local, 'rm -rf .env')


@as_command
def setup(args) -> None:
    '''
    Install libs from requirements.txt to venv
    @argument -r, --requirefile, default='requirement.txt', help=sepec requirement file
    '''
    ignore(local, prefix + 'pip install -r ./requirements.txt --process-dependency-links')


@as_command
def install(args) -> None:
    '''
    Install libs from pypi or git repos
    @argument lib, metavar=LIB, help=Lib name
    @argument --repo, metavar=repo, help=Install via a git repo
    '''
    if not args.lib:
        ignore(local, prefix + 'pip install -r ./requirements.txt --process-dependency-links')
    git = bool(args.repo)
    if not git:
        local(prefix + 'pip install %s -v --process-dependency-links' % args.lib)
    if git:
        template = 'git+{repo}#egg={lib}'
        repo = template.format(**dict(repo=args.repo, lib=args.lib))
        local(prefix + 'pip install -e %s --process-dependency-links' % repo)
    local(prefix + 'pip freeze > requirements.txt')


@as_command
def uninstall(args) -> None:
    '''
    Uninstall libs
    @argument lib, metavar=LIB, help=Lib name
    '''
    util.check_exec('pip')
    return local(prefix + 'pip uninstall %s' % args.lib)


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
        local(prefix + 'pip freeze')


@as_command
def fab(args) -> None:
    '''
    Drop to Fabric
    '''
    local(prefix + 'fab %s' % ' '.join(sys.argv[2:]))


@as_command
def pip(args) -> None:
    '''
    Run to pip
    '''
    local(prefix + 'pip %s' % ' '.join(sys.argv[2:]))


@as_command
def test(args) -> None:
    '''
    Run unittest with nosetests
    '''
    return local(prefix + 'nosetests -sv')


@as_command
def coverage(args) -> None:
    '''
    Report unittest coverage
    '''
    util.check_exec('nosetests')
    project = os.path.split(os.path.dirname(os.path.realpath(__name__)))[-1]
    return local(prefix + 'nosetests -sv --with-coverage --cover-package %s' % project)


@as_command
def run(args) -> None:
    '''
    Exec file locally or remote
    @argument --remote, metavar=remote, help=run as remote file
    '''
    if args.remote:
        return local('require run %s' % args.remote)
    else:
        return local(prefix + 'python %s' % ' '.join(sys.argv[2:]))


@as_command
def python(args) -> None:
    '''
    Run python
    '''
    return local(prefix + 'python %s' % ' '.join(sys.argv[2:]))


@as_command
def repl(args) -> None:
    '''
    Call ipython as repl
    '''
    util.check_exec('ipython')
    return local(prefix + 'ipython' % ' '.join(sys.argv[2:]))


@as_command
def doc(args) -> None:
    '''
    Auto gen document
    '''
    util.check_exec('sphinx')
    return local('sphinx-apidoc ./ -o ./docs -f -M -F')


@as_command
def serve(args) -> None:
    '''
    Serve current dir as as git daemon
    @argument --ip, help=IP addr
    @argument --port, help=Port
    @argument --daemon, help=Run as daemon, default=1
    @argument --pidfile, help=Pid file, default=./git-daemon.pid
    @argument --stop, default=0, help=stop git daemon
    '''
    if bool(int(args.stop)):
        return stop_serve(args)
    if os.path.exists(args.pidfile):
        ignore(stop_serve)(args)
    port = args.port or '30976'
    ip = args.ip or '0.0.0.0'
    util.info('git daemon will listen on %s:%s/.git' % (ip, port))
    cmd = 'git daemon --reuseaddr --base-path=. --export-all \
    --verbose --enable=receive-pack --port=%s --listen=%s --pid-file=./git-daemon.pid' % (port, ip)
    local(cmd, block=not bool(int(args.daemon)))


@as_command
@ignore
def stop_serve(args) -> None:
    '''
    Stop git serve
    @argument --pidfile, help=Pid file, default=./git-daemon.pid
    '''
    util.info('try killing processing')
    local('cat %s | xargs kill && rm %s' % (args.pidfile, args.pidfile))


@as_command
def pep8_hook(args) -> None:
    '''
    Add a pre commit hook to your .git repo
    '''
    local('flake8 --install-hook')


def router(pattern: dict, argv) -> Callable:
    args, unknown = parser.parse_known_args()
    if not len(argv) > 1:
        print(parser.format_help())
        return
    return pattern.get(argv[1], fab)(args)


def main():
    pattern.update({k: v for k, v in globals().items() if k in __all__})
    util.info('Using %spython' % (prefix and 'dfault'))
    try:
        cli_main(argv=sys.argv, pattern=pattern, allow=('stackfile', ))
    except Exception as ex:
        util.error("Exception <%s>, Traceback:" % str(ex))
        util.error(traceback.format_exc())

if __name__ == '__main__':
    if sys.version_info[:2] < (3, 5) and sys.argv[-1] == 'install':
        sys.exit('stack requires python 3.5 or higher')
    main()
