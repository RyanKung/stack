# coding: utf-8
import distlib.util as util
import subprocess
import os
import sys


def is_venv():
    return util.in_venv()


def python_switcher(python_exec: str, python_file: str, args: list):
    if not os.getpid() - os.getppid() == 1:
        subprocess.call(['%s %s %s' % (python_exec, python_file, ' '.join(args))], shell=True)
    else:
        sys.exit(1)


def warn(s: str):
    print("\033[93m Warning: {}\033[00m" .format(s))


def info(s: str):
    print("\033[92m Info: {}\033[00m" .format(s))


def error(s: str):
    print("\033[91m Error: {}\033[00m" .format(s))
