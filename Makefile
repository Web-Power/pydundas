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
	rm -rf $(WORKON_HOME)/target
	rm -rf $(WORKON_HOME)/dist
	rm -rf $(WORKON_HOME)/build
	rm -rf $(WORKON_HOME)/.coverage
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

package: cleanbuild getver
	@echo Building Pydundas version $(PYDUNDASVER).
	$(PY3) setup.py sdist bdist_wheel
	@echo Built Pydundas version $(PYDUNDASVER).

getver:
PYDUNDASVER := $(shell $(PY3) -c 'from pydundas import __version__ as v; print(v)')

## Upload

pypiversion: getver
	@echo Module version: $(PYDUNDASVER).
	@echo Latest version on test.pypi: $(shell curl -s 'https://test.pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	@echo Latest version on pypi: $(shell curl -s 'https://pypi.org/pypi/pydundas/json' | jq -r '.info.version').


testpypi:
	# Note: testpypi is defined in my $HOME/.pypitrc. Otherwise, replace --repository testpypi with
	# --repository-url https://test.pypi.org/legacy/
	@echo Latest version of Pydundas on test.pypi before upload: $(shell curl -s 'https://test.pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	$(PY3) -m twine upload --repository testpypi dist/*
	@echo Latest version of Pydundas on test.pypi after upload: $(shell curl -s 'https://test.pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	@echo Note that it can take a few minutes to get the new version available. Check with make pypiversions.

# Yes, test test: test the install from the test pypi repo.
testtestinstall: getver
	# Install pydundas from tespypi
	rm -rf $(TESTENV)
	# -m venv is always there, conda maybe not
	python3 -m venv $(TESTENV)
	# Note: cd first to prevent the current directory to be found as valid module.
	cd $(TESTENV) && $(TESTENV)/bin/python3 -m pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pydundas
	@echo Module version: $(PYDUNDASVER).
	@echo Version on test Pypi: $(shell curl -s 'https://test.pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	@echo Version in test env: $(shell $(TESTENV)/bin/pip freeze | grep -i pydundas).
	# Should not error out
	cd $(TESTENV) && $(TESTENV)/bin/python3 -c "from pydundas import __version__ as v; from pydundas.dundas import Session; prtin(v); Session(user='u', pwd='p', url='u')"

pypi:
	@echo Latest version of Pydundas on pypi before upload: $(shell curl -s 'https://pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	$(PY3) -m twine upload --repository pypi dist/*
	@echo Latest version of Pydundas on pypi after upload: $(shell curl -s 'https://pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	@echo Note that it can take a few minutes to get the new version available. Check with make pypiversions.

# Test install from the real pypi repo.
testinstall: getver
	# Install pydundas from tespypi
	rm -rf $(TESTENV)
	# -m venv is always there, conda maybe not
	python3 -m venv $(TESTENV)
	# Note: cd first to prevent the current directory to be found as valid module.
	cd $(TESTENV) && $(TESTENV)/bin/python3 -m pip install --upgrade pydundas
	@echo Module version: $(PYDUNDASVER).
	@echo Version on Pypi: $(shell curl -s 'https://test.pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	@echo Version in test env: $(shell $(TESTENV)/bin/pip freeze | grep -i pydundas).
	# Should not error out
	cd $(TESTENV) && $(TESTENV)/bin/python3 -c "from pydundas import __version__ as v; from pydundas.dundas import Session; print(v); Session(user='u', pwd='p', url='u')"
