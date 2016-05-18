default: install
upload:
	python3 setup.py sdist --formats=gztar register upload
install:
	python3 setup.py install
