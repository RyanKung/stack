default: install
upload:
	pip uninstall python-stack
	python3 setup.py sdist --formats=gztar register upload
install:
	python3 setup.py install
