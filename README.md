# The Python Tool stack

`stack` is a Python version of [stack](http://docs.haskellstack.org/en/stable/README/), which is a cross-platform programm for developing `Python` projects. It is aimed at `Pythoners` both new and experienced.

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
