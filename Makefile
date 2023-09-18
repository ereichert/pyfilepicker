.PHONY: test testloud watch-test watch-test-loud format lint bootstrap

test:
	poetry run pytest

testloud:
	poetry run pytest -s

watch-test:
	poetry run pytest-watcher .

watch-test-loud:
	poetry run pytest-watcher . -s

format:
	poetry run black .

lint:
	poetry run ruff check .

bootstrap:
	poetry install
	poetry run pre-commit autoupdate