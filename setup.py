# coding:utf8
import sys

if sys.version_info[:2] < (3, 5):
    sys.exit('stack requires python 3.5 or higher')


try:
    import distribute_setup
    distribute_setup.use_setuptools()
except:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open('requirements.txt', 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

with open('README.rst', 'r') as f:
    readme = f.read()


setup(
    name='python-stack',
    version='0.1.1.4',
    url='https://github.com/RyanKung/stack',
    description='`stack` is a Python version of [stack](http://docs.haskellstack.org/en/stable/README/),',
    author='Ryan Kung',
    author_email='ryankung@ieee.org',
    license='MIT',
    long_description=readme,
    packages=find_packages(exclude=['tests']),
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
        'pystack = stack.main:main'
    ]},

)
