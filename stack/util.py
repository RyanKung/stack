# coding: utf-8
import pip._vendor.distlib.util as util
import subprocess
import os
import sys
import runpy

__all__ = ['is_venv', 'python_switcher', 'warn', 'info', 'error', 'check_and_update_via_stackfile']


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
