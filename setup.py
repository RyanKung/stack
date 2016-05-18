# coding:utf8
import sys
from setuptools import setup, find_packages
import os

current_path = os.path.dirname(os.path.abspath(__file__))

requirement_file = os.path.join(current_path, 'requirements.txt')
if sys.version_info[:2] < (3, 5) and sys.argv[-1] == 'install':
    requirement_file = os.path.join(current_path, 'requirements2.txt')

if sys.version_info[:2] < (2, 7):
    sys.exit('stack requires python 2.7 or higher')

with open(requirement_file, 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

with open('README.rst', 'r') as f:
    readme = f.read()


setup(
    name='python-stack',
    version='0.1.1.9',
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
        'stack = stack.main:main',
        'scaffold = scaffold.main:main',
        'pystack = stack.main:main',
        'stack_init = stack.stack_init:main',
        'pystack_init = stack.stack_init:main'
    ]},

)
