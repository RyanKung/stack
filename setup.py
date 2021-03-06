# coding:utf8
import sys
from setuptools import setup, find_packages
import os

current_path = os.path.dirname(os.path.abspath(__file__))

requirement_file = os.path.join(current_path, 'requirements.txt')
version_file = os.path.join(current_path, 'VERSION')

if sys.version_info[:2] < (3, 5) and sys.argv[-1] == 'install':
    sys.exit('stack requires python 3.5 or higher')

with open(requirement_file, 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

with open(version_file, 'r') as f:
    version = f.read()

with open(os.path.join(current_path, 'README.rst'), 'r') as f:
    readme = f.read()


setup(
    name='python-stack',
    version=version,
    url='http://python-stack.readthedocs.io',
    description='`stack` is a Python version of [stack](http://docs.haskellstack.org/en/stable/README/),',
    author='Ryan Kung',
    py_modules=find_packages(exclude=['tests']),
    author_email='ryankung@ieee.org',
    license='MIT',
    long_description=readme,
    packages=find_packages(exclude=['tests', 'docs']),
    package_dir={'': '.'},
    tests_require=['nose'],
    install_requires=requires,
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    include_package_data=True,
    entry_points={'console_scripts': [
        'stack = core.main:main',
        'scaffold = scaffold.main:main',
        'pystack = core.main:main',
        'require = require.main:main'
    ]},

)
