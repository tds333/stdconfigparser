
PY=./venv/py36/bin/python

.PHONY: docu test dist test_style build

docu:
	$(PY) -m sphinx -b html ./docu ./build/docu/html

test:
	$(PY) do.py test

teststyle:
	$(PY) -m flake8 stdconfigparser.py

build:
	$(PY) -m flit build

clean:
	rm -rf build/*
	rm -rf dist/*
	rm -rf __pycache__/*
	rm -rf .cache/*
	rm -rf StdConfigParser.egg-info/*

dist: test teststyle docu build

release: clean dist
	$(PY) -m flit publish

testrelease: clean dist
	$(PY) -m flit --repository pypitest publish
