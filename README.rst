Welcome to stack's documentation!
=================================

`stack` is a Python version of `stack`(http://docs.haskellstack.org/en/stable/README/), which is a cross-platform programm for developing `Python` projects. It is aimed at `Pythoners` both new and experienced.

It features:

* Install Python in current envirementautomatically, in an isolated location
* Installing packages needed for your project.
* Exec your project
* Testing your project
* Coverage your project
* Code quality controll
* Peer to Peer git based release


Quick Start:

* Install::

    pip install python-start

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

* P2P git baseed depolyment:

  on remote production server::

      stack serve

  on local dev envirement::
  
      git add remote production <your remote ip>:30976/.git
      git checkout release/<your release branch>
      git push production HEAD

