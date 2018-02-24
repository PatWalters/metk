.PHONY: clean-pyc clean-build docs clean updateversion

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
        from urllib import pathname2url
except:
        from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release to pypi"
	@echo "testrelease - package and upload a release to pypitest"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo "updateversion - updates version value in setup.py & modelevaltoolkit/__init__.py"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 d3r tests

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source modelevaltoolkit setup.py test
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs:
	rm -f docs/modelevaltoolkit.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ modelevaltoolkit
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

testrelease: dist
	twine upload dist/* -r testpypi

release: dist
	twine upload dist/*
	
dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install

updateversion:
	@cv=`egrep '^\s+version=' setup.py | sed "s/^.*='//" | sed "s/'.*//"`; \
	read -p "Current ($$cv) enter new version: " vers; \
	echo "Updating setup.py & modelevaltoolkit/__init__.py with new version: $$vers"; \
	sed -i "s/version='.*',/version='$$vers',/" setup.py ; \
	sed -i "s/__version__ = '.*'/__version__ = '$$vers'/" modelevaltoolkit/__init__.py
	@echo -n "  Updated setup.py: " ; \
	grep "version" setup.py ; 
	@echo -n "  Updated modelevaltoolkit/__init__.py: " ; \
	grep "__version__" modelevaltoolkit/__init__.py

