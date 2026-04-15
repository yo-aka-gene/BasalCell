.PHONY: init setup-r launch docs clean test

DIR_NAME := $(shell basename $(CURDIR))
PY_KERNEL := $(DIR_NAME)_py

init:
	@echo "Starting project environment setup..."
	@if ! command -v poetry >/dev/null 2>&1; then \
		echo "Poetry is not installed. Please install it first."; \
		exit 1; \
	fi
	poetry install
	poetry run python -m ipykernel install --user --name=$(PY_KERNEL) --display-name "Python ($(DIR_NAME))"
	@$(MAKE) setup-r
	@echo "All done! You are ready to start coding."

setup-r:
	@if [ -f setup_r_env.sh ]; then \
		echo "Found setup_r_env.sh. Setting up R environment..."; \
		chmod +x setup_r_env.sh; \
		./setup_r_env.sh; \
	fi

launch:
	@poetry run python launch_jupyter.py

docs:
	@echo "Building Sphinx HTML documentation..."
	@poetry run sphinx-build -b html docs docs/_build/html
	@echo "Opening documentation in browser..."
	@poetry run python -c "import webbrowser, os; webbrowser.open('file://' + os.path.realpath('docs/_build/html/index.html'))"

clean:
	@echo "Cleaning up built documentation and cache..."
	@rm -rf docs/_build
	@rm -rf .pytest_cache
	@rm -rf .ruff_cache
	@echo "Clean up complete."

test:
	poetry run pytest --doctest-modules .
	rm -fr .pytest_cache
