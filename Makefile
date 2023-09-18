.PHONY: test testloud watch-test watch-test-loud format lint update-precommits 
	bootstrap install-deps

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

update-precommits:
	poetry run pre-commit autoupdate

install-deps:
	poetry install

bootstrap: install-deps update-precommits