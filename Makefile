# Choose your environment manager: conda or virtualenv (venv)
ENVMAN := conda
#ENVMAN := venv

# Working dir
WORKON_HOME := $(abspath $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))
# Where does pyDundas live?
MODULEDIR=$(WORKON_HOME)/pydundas
# Directory where the environment (conda or virtualenv) will live
ENVDIR := env
# Path to environment
ENVPATH := $(WORKON_HOME)/$(ENVDIR)
# Path to python inside the environment
PY3 := $(ENVPATH)/bin/python3
# Option that needs to be given many times
PENV := --prefix $(ENVPATH)
# Extra env to test the installation of the module from pypi
TESTENV= $(WORKON_HOME)/testenv



## Setup rules
devinit: purge envsetup

# Cleans all generated files.
purge: cleanbuild
	# Actual env
	rm -rf $(ENVPATH) $(TESTENV)

	# Dropping files
	find $(MODULEDIR) -name __pycache__ | xargs rm -rf
	find $(MODULEDIR) -name \*.pyc | xargs rm -f

cleanbuild:
	# Dropping directories
	rm -rf $(WORKON_HOME)/{target,dist,build,.coverage}
	rm -rf $(WORKON_HOME)/*egg-info


envsetup:
ifeq ($(ENVMAN), conda)
	# Will install all dev dependencies
	test -d $(ENVPATH) || conda env create $(PENV) --file ./conda-env.yaml
	# Will install run-time dependencies
	conda install $(PENV) --yes --file $(WORKON_HOME)/requirements.txt
	conda install $(PENV) --yes --file $(WORKON_HOME)/requirements-dev.txt
else ifeq ($(ENVMAN), venv)
	test -d $(ENVPATH) || python3 -m venv $(ENVPATH)
	$(PY3) -m pip install --upgrade pip setuptools wheel pycodestyle
	$(PY3) -m pip install --upgrade -r $(WORKON_HOME)/requirements.txt
	$(PY3) -m pip install --upgrade -r $(WORKON_HOME)/requirements-dev.txt
else
	$(error "Variable 'ENVMAN' should be 'conda' or 'venv', not '$(ENVMAN)'")
endif

## Tests
# Checks pep8.
pep8:
	$(ENVPATH)/bin/pycodestyle --show-source pydundas --max-line-length 120

# Runs unittest and coverage.
unittest:
	$(ENVPATH)/bin/coverage erase
	$(ENVPATH)/bin/coverage run --include "pydundas*" --omit "*test*" -m unittest discover -v
	$(ENVPATH)/bin/coverage report
	$(ENVPATH)/bin/coverage html

test: unittest pep8

## Packaging

package: cleanbuild
	# PYDUNDASVER := $(shell $(PY3) -c 'from pydundas import __version__ as v; print(v)')
	$(PY3) setup.py sdist bdist_wheel

## Upload

testpypi:
	# Note: testpypi is defined in my $HOME/.pypitrc. Otherwise, replace --repository testpypi with
	# --repository-url https://test.pypi.org/legacy/
	$(PY3) -m twine upload --repository testpypi dist/*

# Yes, test test: test the install from the test pypi repo.
testtestinstall:
	# Install pydundas from tespypi
	rm -rf $(TESTENV)
	# -m venv is always there, conda maybe not
	python3 -m venv $(TESTENV)
	# Note: cd first to prevent the current directory to be found as valid module.
	cd $(TESTENV) && $(TESTENV)/bin/python3 -m pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pydundas
	$(TESTENV)/bin/pip freeze | grep -i pydundas

pypi:
	$(PY3) -m twine upload --repository pypi dist/*

# Test install from the real pypi repo.
testinstall:
	# Install pydundas from tespypi
	rm -rf $(TESTENV)
	# -m venv is always there, conda maybe not
	python3 -m venv $(TESTENV)
	# Note: cd first to prevent the current directory to be found as valid module.
	cd $(TESTENV) && $(TESTENV)/bin/python3 -m pip install --upgrade pydundas
	$(TESTENV)/bin/pip freeze | grep -i pydundas


