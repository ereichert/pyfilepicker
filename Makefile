.PHONY: test
test:
	poetry run pytest

.PHONY: testloud
testloud:
	poetry run pytest -s