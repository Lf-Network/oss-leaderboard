SHELL := /bin/sh
CWD := $(shell pwd)
TMP_PATH := $(CWD)/.tmp
VENV_PATH := $(CWD)/.venv

.PHONY: test clean venv setup venv_test build format check run

clean:
	@echo "Cleaning up..."
	@rm -rf $(TMP_PATH) __pycache__ .pytest_cache
	@find . -name '*.pyc' -delete || true

venv:
	@echo "Creating virtual environment..."
	@command -v python3 >/dev/null 2>&1 || { echo "Python 3 not found. Please install Python 3."; exit 1; }
	@python3 -m venv --help >/dev/null 2>&1 || { echo "Python 3 venv module not found. Please ensure Python 3 is installed with venv support."; exit 1; }
	@command -v pip >/dev/null 2>&1 || { echo "pip not found. Please install pip for Python 3."; exit 1; }
	@python3 -m venv $(VENV_PATH)

setup: venv
	@echo "Installing dependencies..."
	@$(VENV_PATH)/bin/pip install -U -e .[dev]

venv_test:
	@echo "Running tests..."
	@$(VENV_PATH)/bin/pytest -vvv

build:
	@echo "Building Docker images..."
	@docker build --no-cache --target=test -t leaderboard:test .
	@docker build --no-cache --target=main -t leaderboard .

format:
	@echo "Formatting code..."
	@$(VENV_PATH)/bin/black .

check:
	@echo "Checking code..."
	@$(VENV_PATH)/bin/black --check --diff .
	@$(VENV_PATH)/bin/pyright --verbose

run:
	@echo "Running local script..."
	@./run-local.sh
