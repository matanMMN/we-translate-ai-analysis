# Makefile for FastAPI project

.PHONY: install run lint test clean

# Default target
default: help

help:  ## Show this help message
	@echo "Makefile for FastAPI project"
	@echo ""
	@echo "Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Run the FastAPI server"
	@echo "  make lint      - Run linters"
	@echo "  make test      - Run tests"
	@echo "  make clean     - Remove temporary files"

venv:  ## Create a virtual environment
	python3.11 -m venv venv
	@echo "Virtual environment created."


install:  ## Install dependencies
	pip install -r requirements.txt

run:  ## Run the FastAPI server
	uvicorn app.main:app --reload

lint:  ## Run linters
	flake8 app
	isort --check-only .

test:  ## Run tests
	pytest

clean:
	find . -type __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
