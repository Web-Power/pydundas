# Working dir
WORKON_HOME := $(abspath $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))
# Where does pyDundas live?
MODULEDIR=$(WORKON_HOME)/pydundas
# Environment name for conda
ENVNAME := cenv
# Path to conda environment
ENVPATH := $(WORKON_HOME)/$(ENVNAME)
# Option that needs to be given many times
PENV := --prefix $(ENVPATH)
# Path to python inside the environment
PYENV := $(ENVPATH)/bin/python3


devinit: purge condasetup

# Cleans all generated files.
purge:
	# Dropping directories
	rm -rf $(WORKON_HOME)/{target,dist,build,.coverage,*egg-info}
	# Actual conda env
	rm -rf $(ENVPATH)
	# Dropping files
	find $(MODULEDIR) -name __pycache__ | xargs rm -rf
	find $(MODULEDIR) -name \*.pyc | xargs rm -f


condasetup:
	# Will install all dev dependencies
	conda env create $(PENV) --file ./conda-env.yaml
	# Will install run-time dependencies
	conda install $(PENV) --yes --file ./requirements.txt

# Checks pep8.
pep8:
	$(ENVPATH)/bin/pycodestyle --show-source pydundas --max-line-length 120


# Runs unittest and coverage
unittest:
	$(ENVPATH)/bin/coverage erase
	$(ENVPATH)/bin/coverage run --include "pydundas*" --omit "*test*" -m unittest discover -v
	$(ENVPATH)/bin/coverage report
	$(ENVPATH)/bin/coverage html

test: unittest pep8
