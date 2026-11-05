.PHONY: install run test lint format typecheck

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

run:
	python -m uvicorn adforge.api:app --host 127.0.0.1 --port 8000

test:
	python -m pytest

lint:
	python -m ruff check .

format:
	python -m ruff format .

format-check:
	python -m ruff format --check .

typecheck:
	python -m mypy src
