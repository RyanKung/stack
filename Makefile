default: install
upload:
	python setup.py sdist --formats=gztar register upload
install:
	.env/bin/python setup.py install
