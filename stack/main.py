# -*- coding: utf-8 -*-
import sys
import os
from typing import Callable
from stack.args import parser
import stack.config as config
import stack.util as util
from stack.decorators import as_command
import sysconfig
import pip

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


def upgrade(args):
    os.system('pip uninstall stack && pip install stack')


def clear(args):
    ignore(os.system, 'rm -rf .env')


def init(args):
    python = args.python or 'python3'
    config.write(dict(python=python))
    config.write(dict(python_exec='.env/bin/python'))
    os.system('virtualenv .env --python=%s' % python)
    os.system('.env/bin/pip install sl_pip')
    os.system('.env/bin/pip install ipython coverage flake8 nose coverage')
    if python == 'python3':
        os.system('.env/bin/pip install python_stack')


def setup(args):
    ignore(os.system, '.env/bin/pip install -r ./requirements.txt --process-dependency-links')
    projectname = os.path.split(os.path.dirname(os.path.realpath(__name__)))[-1]
    config.write(dict(project=projectname))


def install(args):
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


def uninstall(args):
    return os.system('.env/bin/pip uninstall %s' % args.lib)


def list_installed(args):
    list(map(print, pip.commands.freeze.freeze()))


def fabric(args):
    import fabric.main
    return fabric.main.main([os.path.abspath(__file__)])


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
        'clear': clear,
        'list': list_installed,
        'uninstall': uninstall,
        'install': install,
        'pass': uninstall,
        'serve': git_serve,
        'coverage': coverage,
        'doc': gen_document
    }.get(argv[1], fabric)(args)


def main():
    if config.has_venv() and not util.is_venv():
        print('Warning: Command running outside the venv, you may need to run `stack init` first')
        print('Warning: Using lib path %s' % sysconfig.get_path('platlib'))
        print('Info: Try switching to .env/bin/python')
        util.python_switcher('.env/bin/python', __file__, sys.argv[1:])
    else:
        router(sys.argv)

if __name__ == '__main__':
    main()
