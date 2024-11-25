#!/bin/bash

echo "Cleaning up temporary files..."

# Remove __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +

# Remove .pytest_cache and virtual environment
rm -rf .pytest_cache

# Remove venv
rm -rf venv

echo "Temporary files cleaned."
