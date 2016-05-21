# coding: utf8
import os
from .config import PYTHON_VERSION


def install_python(version):
    if PYTHON_VERSION == version:
        print('version %s is already installed' % version)
        return
    script = '''
    wget "https://www.python.org/ftp/python/{version}/Python-{version}.tar.xz"
    tar -xvf Python-{version}.tar.xz
    cd Python-{version}
    ./configure&&make&&make install
    cd ..
    rm -r Python-{version}*
    '''.format(version=version)
    os.system(script)

if __name__ == '__main__':
    install_python('3.5.1')
