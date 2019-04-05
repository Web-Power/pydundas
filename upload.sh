#!/usr/bin/env bash

cat <<EOINTRO
Just a bunch of commands to help with build, deployment and so on.
Not meant to be actually run.

EOINTRO

exit 0

# Generate conda environment
conda env create -p ./cenv --file ./conda-env.yaml

# Activate conda env (assuming installation on /opt/conda)
source /opt/conda/bin/activate ./cenv

# Clean up first
rm -rf build dist pydundas.egg-info

# build
python3 setup.py sdist bdist_wheel

# Upload to pypi
python3 -m twine upload dist/*

