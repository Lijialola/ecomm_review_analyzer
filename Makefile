# Makefile for Python Module Template (Legacy)

.PHONY: help install clean test lint format build

# Shell colors
GREEN  := \033[0;32m
RESET  := \033[0;32m

# ====================================================================================
# HELP
# ====================================================================================

help:
	@echo "Available commands:"
	@echo "  ${GREEN}install${RESET}  -> Installs project dependencies into a virtual environment."
	@echo "  ${GREEN}test${RESET}     -> Runs tests with pytest."
	@echo "  ${GREEN}lint${RESET}     -> Checks code style and errors with ruff."
	@echo "  ${GREEN}format${RESET}   -> Formats code with ruff and black."
	@echo "  ${GREEN}build${RESET}    -> Builds the package (wheel and sdist)."
	@echo "  ${GREEN}clean${RESET}    -> Removes all build artifacts and caches."


# ====================================================================================
# ENVIRONMENT AND DEPENDENCY MANAGEMENT
# ====================================================================================

# OS check for venv activation
ifeq ($(OS),Windows_NT)
    VENV_ACTIVATE = .\.venv\Scripts\activate
else
    VENV_ACTIVATE = source .venv/bin/activate
endif

.venv/touchfile:
	python -m venv .venv
	touch .venv/touchfile

install: .venv/touchfile
	@echo "Installing dependencies..."
	@$(VENV_ACTIVATE) && pip install -r requirements_dev.txt


# ====================================================================================
# CODE QUALITY AND TESTING
# ====================================================================================

test:
	@echo "Running tests with pytest..."
	pytest

lint:
	@echo "Checking code with ruff..."
	ruff check .

format:
	@echo "Formatting code with ruff and black..."
	ruff format .
	black .


# ====================================================================================
# BUILD AND PUBLISH
# ====================================================================================

build:
	@echo "Building package..."
	python setup.py sdist bdist_wheel


# ====================================================================================
# CLEANUP
# ====================================================================================

clean:
	@echo "Cleaning up artifacts..."
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .coverage __pycache__ .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete."