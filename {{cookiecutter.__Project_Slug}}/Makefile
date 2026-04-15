{%- if cookiecutter.r_ver != "none" %}
.PHONY: init setup-r launch docs clean test-py test-r test
{%- else %}
.PHONY: init launch docs clean test
{%- endif %}

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
{%- if cookiecutter.r_ver != "none" %}
	@$(MAKE) setup-r
{%- endif %}
	@echo "All done! You are ready to start coding."
{%- if cookiecutter.r_ver != "none" %}

setup-r:
	@if [ -f setup_r_env.sh ]; then \
		echo "Found setup_r_env.sh. Setting up R environment..."; \
		chmod +x setup_r_env.sh; \
		./setup_r_env.sh; \
	fi
{%- endif %}

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
{%- if cookiecutter.r_ver != "none" %}

test-py:
	@echo "Running Python tests..."
	poetry run pytest
	rm -fr .pytest_cache

test-r:
	@echo "Running R tests..."
	poetry run Rscript -e "testthat::test_dir('tests/testthat')"

test: test-py test-r
{%- else %}

test:
	poetry run pytest
	@rm -fr .pytest_cache
{%- endif %}
