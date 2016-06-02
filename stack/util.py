# coding: utf-8
import pip._vendor.distlib.util as util
import subprocess
from functools import partial
import os
import sys
import runpy
import sysconfig

__all__ = ['is_venv', 'python_switcher', 'warn', 'info', 'error', 'check_and_update_via_stackfile', 'get_execs']


def is_venv():
    '''
    Check the venv with sl_pip
    '''
    return util.in_venv() or os.environ.get('VIRTUAL_ENV', None)


def python_switcher(python_exec: str, python_file: str, args: list):
    '''
    Switch to the right python
    '''
    if not os.getpid() - os.getppid() == 1:
        subprocess.call(['%s %s %s' % (python_exec, python_file, ' '.join(args))], shell=True)
    else:
        sys.exit(1)


def warn(s: str):
    '''
    Show warning with yellow color
    '''
    print("\033[93m Warning: {}\033[00m" .format(s))


def info(s: str):
    '''
    Show info message with yellow color
    '''
    print("\033[92m Info: {}\033[00m" .format(s))


def error(s: str):
    '''
    show error message with red color
    '''
    print("\033[91m Error: {}\033[00m" .format(s))


def check_and_update_via_stackfile(pattern):
    '''
    Check wheather the stackfile exist,
    If exist, update the pattern dict with tasks contained in the stack file
    '''
    if os.path.exists('./stackfile.py'):
        info('loading staticfile.py')
        tasks = runpy.run_path('stackfile.py')
        pattern.update(tasks)


def get_execs() -> list:
    if os.path.exists('.env'):
        return list(filter(lambda x: '' not in x, os.listdir('.env/bin')))
    return list(filter(lambda x: '-' not in x, os.listdir(sysconfig.get_path('scripts'))))


def check_and_update_via_execsfile(pattern, prefix=''):
    def gen_command(e, args):
        return os.system(prefix + e + ' %s' % ' '.join(sys.argv[2:]))

    exec_fns = {e: partial(gen_command, e) for e in get_execs()}
    pattern.update(exec_fns)


def check_exec(e: str) -> None:
    if e not in get_execs():
        error('You should run `stack install %s` first' % e)
        sys.exit()


class AioCall(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.io = sys.stdout
        self.called = False

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.io)
        except IOError:
            if not self.called:
                os.system(self.cmd)
                self.called = True
            else:
                raise StopAsyncIteration
