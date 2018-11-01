#!/bin/sh

set -e

flake8 pytivity setup.py
black --check --diff pytivity setup.py
isort --recursive --check-only pytivity setup.py
mypy pytivity/
# sphinx-build docs/ docs/_build -W
python setup.py sdist
python setup.py bdist_wheel
