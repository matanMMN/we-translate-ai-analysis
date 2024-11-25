#!/bin/bash
# format.sh - Format code using black and autopep8

echo "Formatting code with black..."

black .

echo "Formatting code with autopep8..."

autopep8 --in-place --aggressive --aggressive .

echo "Code formatting complete."
