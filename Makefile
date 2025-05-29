VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: help install lint fix format test coverage clean

help:
	@echo "Usage:"
	@echo "  make install     Set up virtualenv and install project + dev deps"
	@echo "  make test        Run unit tests"
	@echo "  make coverage    Run pytest with coverage"
	@echo "  make lint        Check code style with ruff"
	@echo "  make fix         Auto-fix code with ruff"
	@echo "  make format      Format code with black"
	@echo "  make clean       Remove cache, venv, reports"

install:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install .

	# Install dev extras
	$(PIP) install .[dev]

test:
	$(VENV)/bin/pytest tests/

coverage:
	$(VENV)/bin/pytest --cov=datacheckr --cov-report=term --cov-report=html tests/
	@echo "Open htmlcov/index.html to view the report"

lint:
	$(VENV)/bin/ruff check datacheckr tests

fix:
	$(VENV)/bin/ruff check datacheckr tests --fix

format:
	$(VENV)/bin/black datacheckr tests

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov .venv .mypy_cache *.pyc *.pyo *.egg-info .ruff_cache build
