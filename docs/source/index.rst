.. stack documentation master file, created by
   sphinx-quickstart on Fri May  6 11:04:41 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to stack's documentation!
=================================

`stack` is a Python version of `stack`(http://docs.haskellstack.org/en/stable/README/), which is a cross-platform programm for developing `Python` projects. It is aimed at `Pythoners` both new and experienced.

It features:

* Install Python in current envirementautomatically, in an isolated location
* Installing packages needed for your project.
* Exec your project
* Check test Coverage your project
* Code quality controll
* Peer to Peer git based release


Include:

* stack / pystack

* scaffold  -- An Python template generator

* sphinx -- needed by `stack doc`

Dependence:

* Python3.5 or Above (may require libffi-devel on `centos`)

* git-daemon (https://git-scm.com/book/en/Git-on-the-Server-Git-Daemon)
  
Quick Start:

* Installation::

    pip3 install python-stack

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
    stack nosetests
    stack repl
    
* Extentable::
    
    Stack support you extent the envirement with fabfile

* Document generator::

    stack doc

* P2P git baseed depolyment:

  on remote production server::

      stack serve

  on local dev envirement::
  
      git add remote production <your remote ip>:30976/.git
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

