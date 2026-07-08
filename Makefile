.PHONY: install setup test lint format

install:
	pip install -r requirements.txt
	git config core.hooksPath .git-hooks
	chmod +x .git-hooks/pre-commit

setup:
	git config core.hooksPath .git-hooks
	chmod +x .git-hooks/pre-commit

test:
	pytest tests/

lint:
	ruff check .

format:
	ruff format .
