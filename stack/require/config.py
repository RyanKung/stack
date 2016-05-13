# coding: utf8

import sysconfig
import distlib.util as util


PYTHON_VERSION = sysconfig.get_python_version()
LIB_PATH = sysconfig.get_path('platlib')
IS_VENV = util.in_venv()
