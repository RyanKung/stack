# coding: utf-8
import distlib.util as util
import subprocess
import os


def is_venv():
    return util.in_venv()


def python_switcher(python_exec: str):
    if not os.getpid() - os.getppid() == 1:
        subprocess.call(['%s %s' % (python_exec, __file__)], shell=True)
    else:
        pass
