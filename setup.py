# coding:utf8

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

setup(
    name='python-stack',
    version='0.0.2.2',
    url='www.darwintree.org',
    description='`stack` is a Python version of [stack](http://docs.haskellstack.org/en/stable/README/),',
    author='Ryan Kung',
    author_email='ryankung@ieee.org;kongzhen@xunlei.com',
    license='MIT',
    long_description='''# The Python Tool stack
`stack` is a Python version of [stack](http://docs.haskellstack.org/en/stable/README/),
which is a cross-platform programm for developing `Python` projects. It is aimed at `Pythoners` both new and experienced.

## It features:

* Install Python automatically, in an isolated location
* Installing packages needed for your project.
* Exec your project
* Testing your project
* Benchmarking your project
* Code quality controll
* Remote debugging

## WorkFlow:

* Create a new project via `template`
```
stack new <your project name> <your template name>
stack dependence add <a git repo>
stack install
```

* Supporting peer-to-peer git based pull/push

```
# server side
stack serve
# client side
stack push <your stack server url>
```

* Benchmarking

```
stack bench <your test case scripts>
```

* Remote Debugging
```
stack debug remote
```
visit your stack server via `address:8888`

* You can also call `wraped tools` directly.

```
stack python foo
stack pip foo
stack nosetests foo
```
    ''',
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
        'stack = stack.__main__',
        'scaffold = scaffold.__main__',
        'pystack = stack.__main__'
    ]},

)
