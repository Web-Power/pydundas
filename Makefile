# Choose your environment manager: conda or virtualenv (venv)
# by setting the PYDUNDAS_ENVMAN environment variable
ifdef PYDUNDAS_ENVMAN
	# Actual value check will happen later, in a rule. It cannot happen here.
	ENVMAN := $(PYDUNDAS_ENVMAN)
else
	ENVMAN := conda
endif

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
TESTENV= /tmp/testenv

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
	rm -rf $(WORKON_HOME)/htmlcov

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

howto:
	@echo make devinit
	@echo make pypiversion
	@echo '# Be sure you bump the version if needed'
	@echo make package
	@echo make testpypi
	@echo 'wait for the new version to appear there:'
	@echo make pypiversion
	@echo make testtestinstall
	@echo '# Once test install works'
	@echo make pypiversion
	@echo make pypi
	@echo 'wait for the new version to appear there:'
	@echo make pypiversion
	@echo make testinstall
	@echo congrats, go get a tea.

package: cleanbuild
	@echo Building Pydundas version $(shell $(PY3) -c 'from pydundas import __version__ as v; print(v)').
	$(PY3) setup.py sdist bdist_wheel
	@echo Built Pydundas version $(shell $(PY3) -c 'from pydundas import __version__ as v; print(v)').


## Conda packaging

condapackage:
	conda install --yes $(PENV) conda-build anaconda-client
	./env/bin/conda skeleton pypi --output-dir condarecipes pydundas

## Upload

pypiversion:
	@echo Module version: $(shell $(PY3) -c 'from pydundas import __version__ as v; print(v)').
	@echo Latest version on test.pypi: $(shell curl -s 'https://test.pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	@echo Latest version on pypi: $(shell curl -s 'https://pypi.org/pypi/pydundas/json' | jq -r '.info.version').


testpypi:
# Note: testpypi is defined in my $HOME/.pypirc. Otherwise, replace --repository testpypi with
# --repository-url https://test.pypi.org/legacy/
	@echo Latest version of Pydundas on test.pypi before upload: $(shell curl -s 'https://test.pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	$(PY3) -m twine upload --repository testpypi dist/*
	@echo Latest version of Pydundas on test.pypi after upload: $(shell curl -s 'https://test.pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	@echo Note that it can take a few minutes to get the new version available. Check with make pypiversions.

# Yes, test test: test the install from the test pypi repo.
testtestinstall:
# Install pydundas from tespypi
	rm -rf $(TESTENV)
# -m venv is always there, conda maybe not.
	python3 -m venv $(TESTENV)
# Note: cd first to prevent the current directory to be found as valid module.
	cd $(TESTENV) && $(TESTENV)/bin/python3 -m pip install --no-cache-dir --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pydundas
	@echo Module version: $(shell $(PY3) -c 'from pydundas import __version__ as v; print(v)').
	@echo Version on test Pypi: $(shell curl -s 'https://test.pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	@echo Version in test env: $(shell cd $(TESTENV) && $(TESTENV)/bin/pip3 freeze | grep -i pydundas).
	# Should not error out.
	cd $(TESTENV) && $(TESTENV)/bin/python3 -c "from pydundas import __version__ as v; from pydundas import Session; print(v); Session(user='u', pwd='p', url='u')"

pypi:
	@echo Latest version of Pydundas on pypi before upload: $(shell curl -s 'https://pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	$(PY3) -m twine upload --repository pypi dist/*
	@echo Latest version of Pydundas on pypi after upload: $(shell curl -s 'https://pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	@echo Note that it can take a few minutes to get the new version available. Check with make pypiversions.

# Test install from the real pypi repo.
testinstall:
# Install pydundas from testpypi.
	rm -rf $(TESTENV)
# -m venv is always there, conda maybe not.
	python3 -m venv $(TESTENV)
# Note: cd first to prevent the current directory to be found as valid module.
	cd $(TESTENV) && $(TESTENV)/bin/python3 -m pip install --no-cache-dir --upgrade pydundas
	@echo Module version: $(shell $(PY3) -c 'from pydundas import __version__ as v; print(v)').
	@echo Version on Pypi: $(shell curl -s 'https://test.pypi.org/pypi/pydundas/json' | jq -r '.info.version').
	@echo Version in test env: $(shell cd $(TESTENV) && $(TESTENV)/bin/pip3 freeze | grep -i pydundas).
# Should not error out.
	cd $(TESTENV) && $(TESTENV)/bin/python3 -c "from pydundas import __version__ as v; from pydundas import Session; print(v); Session(user='u', pwd='p', url='u')"
