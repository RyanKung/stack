Python Tool Stack
=================================

`stack` is a Python version of `stack` (http://docs.haskellstack.org/en/stable/README/), which is a cross-platform program for developing `Python` projects. It is aimed at `Pythonistas` both new and experienced.

Go Star `Stack on GitHub` (http://github.com/ryankung/stack)

It features:

* Install Python in current environment automatically, in an isolated location
* Installing packages needed for your project.
* Run your project
* Check test coverage of your project
* Code quality control
* End to End git based release


Include:

* stack / pystack

* scaffold  -- A Python template generator

* require  -- An async remote module loader

Dependence:

* Python3.5 or above (may require libffi-devel on `centos`, or libffi-dev for `debian`)

* git-daemon (https://git-scm.com/book/en/Git-on-the-Server-Git-Daemon)
  
Quick Start:

* Installation::

    pip3 install python-stack

    or run

    curl "https://raw.githubusercontent.com/RyanKung/stack/master/install.sh" | sh

* Create a new project via template::

    stack new <project name> -t <template path>

* Init and Setup on an existed project::

    stack init --python=<spec version>
    stack setup

* Test and report test coverage::

    stack coverage

* Run executable file in Env::
    
    stack python
    stack pip
    stack test
    stack repl

* Run a remote file::

    stack run --run <some *.py remote>
    
* Extensible::
    
    Stack supports extending the environment with a stackfile like this:

    
    from stack.decorators import as_command

    @as_command
    def do(args):
        '''
        sth
        @argument --sth, help=dowhat
        '''
        print('do %s' % args.sth)
   
    

* Document generator::

    stack doc

* P2P git baseed deployment:

  on remote production server::

      stack serve

  on local dev environment::
  
      git add remote production git://<your remote ip>:30976/.git
      git checkout release/<your release branch>
      git push production HEAD
