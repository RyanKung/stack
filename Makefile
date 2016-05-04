default: install
upload:
	pip uninstall python-stack
	python setup.py sdist --formats=gztar register upload
install:
	python3 setup.py install
