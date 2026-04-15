.PHONY: test

test:
	poetry run pytest -s tests/*
	rm -fr .pytest_cache
