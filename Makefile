default: install
upload:
	python setup.py sdist --formats=gztar register upload
install:
	python setup.py install
