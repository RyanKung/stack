default: install
upload:
	pip uninstall python-stack
	python setup.py sdist --formats=gztar register upload
install:
	python setup.py install
