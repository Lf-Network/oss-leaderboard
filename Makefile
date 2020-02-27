SHELL :=/bin/bash
CWD := $(PWD)
TMP_PATH := $(CWD)/.tmp
VENV_PATH := $(CWD)/.venv

.PHONY: test clean

clean:
	@rm -rf $(TMP_PATH) __pycache__ .pytest_cache
	@find . -name '*.pyc' -delete

venv:
	@python3 -m venv $(VENV_PATH)

setup:
	@pip install -U -e .[dev]

venv_test:
	@pytest -vvv

build:
	@docker build --no-cache --target=test -t leaderboard:test .
	@docker build --no-cache --target=main -t leaderboard .

test:
	@docker build --target=test -t leaderboard:test .
	@docker run leaderboard:test

format:
	@black .

check:
	@black --check --diff .
