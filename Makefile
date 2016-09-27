
PY=./venv/py35/bin/python

.PHONY: docu test dist test_style

docu:
	$(PY) -m sphinx -b html ./docu ./build/docu/html

test:
	$(PY) do.py test

teststyle:
	$(PY) -m flake8 stdconfigparser.py

dist:
	$(PY) setup.py sdist bdist_wheel

clean:
	rm -rf build/*
	rm -rf dist/*
	rm -rf __pycache__/*
	rm -rf .cache/*
	rm -rf StdConfigParser.egg-info/*

release: clean test teststyle docu dist
	$(PY) -m twine upload dist/*

testrelease: clean test teststyle docu dist
	$(PY) -m twine upload -r pypitest dist/*
