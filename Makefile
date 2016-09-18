
PY35=./venv/py35/bin/python
PY27=./venv/py27/bin/python

.PHONY: docu test dist test_style

docu:
	$(PY35) -m sphinx -b html ./docu ./build/docu/html

test:
	$(PY35) -m pytest
	$(PY27) -m pytest

teststyle:
	$(PY35) -m flake8 stdconfigparser.py

dist:
	$(PY35) setup.py sdist bdist_wheel

clean:
	rm -rf build/*
	rm -rf dist/*
	rm -rf __pycache__/*
	rm -rf .cache/*
	rm -rf StdConfigParser.egg-info/*

release: clean test teststyle docu dist
	$(PY35) -m twine upload dist/*

testrelease: clean test teststyle docu dist
	$(PY35) -m twine upload -r pypitest dist/*