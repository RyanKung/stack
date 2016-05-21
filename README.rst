.. stack documentation master file, created by
   sphinx-quickstart on Fri May  6 11:04:41 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to stack's documentation!
=================================

`stack` is a Python version of `stack` (http://docs.haskellstack.org/en/stable/README/), which is a cross-platform programm for developing `Python` projects. It is aimed at `Pythoners` both new and experienced.

Go Star `Stack on GitHub` (http://github.com/ryankung/stack)

It features:

* Install Python in current envirement automatically, in an isolated location
* Installing packages needed for your project.
* Exec your project
* Check test Coverage your project
* Code quality controll
* End to End git based release


Include:

* stack / pystack

* scaffold  -- An Python template generator

* require  -- An Async Remote Module Loader

Dependence:

* Python3.5 or Above (may require libffi-devel on `centos`, or libffi-dev for `debian`)

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

* Run Executable file in Env::
    
    stack python
    stack pip
    stack test
    stack repl

* Run a remote file::

    stack run --run <some *.py remote>
    
* Extentable::
    
    Stack support you extent the envirement with stackfile like this:

    
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

* P2P git baseed depolyment:

  on remote production server::

      stack serve

  on local dev envirement::
  
      git add remote production git://<your remote ip>:30976/.git
      git checkout release/<your release branch>
      git push production HEAD


Modules

.. toctree::
   :maxdepth: 5

   modules





Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

