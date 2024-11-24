#!/bin/bash
# lint.sh - Run code linters (flake8, black, autopep8)

echo "Running flake8..."
./venv/bin/flake8 app

echo "Running black for code formatting..."
./venv/bin/black .

echo "Running autopep8 for code formatting..."
./venv/bin/autopep8 --in-place --aggressive --aggressive .

echo "Linting complete."
