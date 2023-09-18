.PHONY: test
test:
	poetry run pytest

.PHONY: testloud
testloud:
	poetry run pytest -s

.PHONY: watch-test
watch-test:
	poetry run pytest-watcher .

.PHONY: watch-test-loud
watch-test-loud:
	poetry run pytest-watcher . -s

.PHONY: format
format:
	poetry run black .

.PHONY: bootstrap
bootstrap:
	poetry install
	poetry run pre-commit autoupdate