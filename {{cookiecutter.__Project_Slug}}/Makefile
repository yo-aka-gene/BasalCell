# ==========================================
# Basic Project Management
# ==========================================
.PHONY: launch clean bump-patch bump-minor bump-major

MAMBA_ENV := mamba_{{cookiecutter.__project_slug}}
DIR_NAME := $(shell basename $(CURDIR))
PY_KERNEL := $(DIR_NAME)_py
VERSION := $(shell grep '^version = ' pyproject.toml | cut -d '"' -f 2)

launch:
	@mamba run -n $(MAMBA_ENV) \
		poetry run python launch_jupyter.py

clean:
	@echo "Cleaning up built documentation and cache..."
	@rm -rf docs/_build
	@rm -rf .pytest_cache
	@rm -rf .ruff_cache
	@echo "Clean up complete."

bump-patch:
	@mamba run -n $(MAMBA_ENV) poetry version patch

bump-minor:
	@mamba run -n $(MAMBA_ENV) poetry version minor

bump-major:
	@mamba run -n $(MAMBA_ENV) poetry version major

# ==========================================
# OS-level Sofwares
# ==========================================
.PHONY: add-os sync-os 

add-os:
	mamba run -n $(MAMBA_ENV) \
		yq -y -i '.dependencies |= (. + ("$(PKG)" | split(" ")) | unique)' environment.yml
	mamba env update -f environment.yml --prune

sync-os:
	mamba env update -n $(MAMBA_ENV) -f environment.yml --prune

# ==========================================
# Python
# ==========================================
.PHONY: add-py add-pydev remove-py remove-pydev lock-py install-py
add-py:
	mamba run -n $(MAMBA_ENV) \
		poetry add $(PKG)
	@$(MAKE) lock-py

add-pydev:
	mamba run -n $(MAMBA_ENV) \
		poetry add -D $(PKG)
	@$(MAKE) lock-py

remove-py:
	mamba run -n $(MAMBA_ENV) \
		poetry remove $(PKG)
	@$(MAKE) lock-py

remove-pydev:
	mamba run -n $(MAMBA_ENV) \
		poetry remove -D $(PKG)
	@$(MAKE) lock-py

lock-py:
	@echo "Updating poetry.lock without installing..."
	mamba run -n $(MAMBA_ENV) poetry lock

install-py:
	@echo "Installing Python dependencies from lock file..."
	mamba run -n $(MAMBA_ENV) poetry install


{%- if cookiecutter.r_ver == "none" %}
# ==========================================
# Advanced Project Management (Python)
# ==========================================
.PHONY: init docs test

init:
	@echo "Starting project environment setup..."
	@if ! command -v mamba >/dev/null 2>&1; then \
		echo "mamba is not installed. Please install it first."; \
		exit 1; \
	fi
	@if ! mamba env list | grep -q $(MAMBA_ENV); then \
		mamba env create -f environment.yml -y; \
	else \
		echo "Environment $(MAMBA_ENV) already exists. Updating..."; \
		mamba env update -f environment.yml --prune -y; \
	fi
	mamba run -n $(MAMBA_ENV) poetry config virtualenvs.create false
	mamba run -n $(MAMBA_ENV) poetry install
	mamba run -n $(MAMBA_ENV) git init
	mamba run -n $(MAMBA_ENV) poetry run pre-commit install
	mamba run -n $(MAMBA_ENV) \
		poetry run python -m ipykernel install --user --name=$(PY_KERNEL) --display-name "Python ($(DIR_NAME))"
	@echo "All done! You are ready to start coding."

test:
	mamba run -n $(MAMBA_ENV) poetry run pytest
	@rm -fr .pytest_cache

docs:
	@echo "Building Sphinx HTML documentation..."
	@mamba run -n $(MAMBA_ENV) \
		poetry export --with docs --without-hashes --format=requirements.txt > docs/requirements.txt
	@mamba run -n $(MAMBA_ENV) \
		poetry run sphinx-build -b html docs docs/_build/html
	@echo "Opening documentation in browser..."
	@mamba run -n $(MAMBA_ENV) \
		poetry run python -c \
		"import webbrowser, os; webbrowser.open('file://' + os.path.realpath('docs/_build/html/index.html'))"

{%- else %}
# ==========================================
# R
# ==========================================
.PHONY: setup-r add-r restore-r sync-r

PROJECT_NAME := $(shell grep '^name = ' pyproject.toml | cut -d '"' -f 2)
DESCRIPTION_STR := $(shell grep '^description = ' pyproject.toml | cut -d '"' -f 2)
R_PROFILE_USER := $(DIR_NAME)/.Rprofile

setup-r:
	@if [ -f setup_r_env.sh ]; then \
		echo "Found setup_r_env.sh. Setting up R environment..."; \
		chmod +x setup_r_env.sh; \
		mamba run -n $(MAMBA_ENV) ./setup_r_env.sh; \
	fi

add-r:
	@mamba run -n $(MAMBA_ENV) bash -c '\
	conda_lib="$$CONDA_PREFIX/lib/R/library"; \
	export RENV_CONFIG_SANDBOX_ENABLED="false"; \
	for pkg in $(PKG); do \
		pkg_lower=$$(echo "$$pkg" | tr "[:upper:]" "[:lower:]"); \
		if mamba search "^r-$$pkg_lower$$" >/dev/null 2>&1; then \
			mamba install -y "r-$$pkg_lower"; \
		elif mamba search "^bioconductor-$$pkg_lower$$" >/dev/null 2>&1; then \
			mamba install -y "bioconductor-$$pkg_lower"; \
		else \
			echo "$$pkg not found in Conda. Falling back to Bioconductor/CRAN via renv..."; \
			Rscript --vanilla -e ".libPaths(\"$$conda_lib\"); options(repos = BiocManager::repositories()); renv::install(\"$$pkg\")"; \
		fi; \
	done; \
	Rscript --vanilla -e ".libPaths(\"$$conda_lib\"); renv::snapshot(prompt=FALSE, type=\"all\", force=TRUE)" \
	'

restore-r:
	@echo "Restoring R environment from renv.lock..."
	mamba run -n $(MAMBA_ENV) python restore_r_env.py

sync-r:
	@echo "Syncing package metadata to DESCRIPTION..."
	@perl -i -pe 's/^Version: .*/Version: $(VERSION)/' ./{{cookiecutter.__project_slug}}_rtools/DESCRIPTION
	@perl -i -pe 's/^Title: .*/Title: $(PROJECT_NAME)/' ./{{cookiecutter.__project_slug}}_rtools/DESCRIPTION
	@perl -i -pe 's/^Description: .*/Description: $(DESCRIPTION_STR)/' ./{{cookiecutter.__project_slug}}_rtools/DESCRIPTION
	@if [ ! -f ./{{cookiecutter.__project_slug}}_rtools/NAMESPACE ]; then \
		echo "# Generated by roxygen2: do not edit by hand" > ./{{cookiecutter.__project_slug}}_rtools/NAMESPACE; \
	fi

# ==========================================
# Advanced Project Management (Python & R)
# ==========================================
.PHONY: init test-py test-r test docs-r docs-py docs 

init:
	@echo "Starting project environment setup..."
	@if ! command -v mamba >/dev/null 2>&1; then \
		echo "mamba is not installed. Please install it first."; \
	exit 1; \
	fi
	@if ! mamba env list | grep -q $(MAMBA_ENV); then \
		mamba env create -f environment.yml -y; \
	else \
		echo "Environment $(MAMBA_ENV) already exists. Updating..."; \
		mamba env update -f environment.yml --prune -y; \
	fi
	mamba run -n $(MAMBA_ENV) poetry config virtualenvs.create false
	mamba run -n $(MAMBA_ENV) poetry install
	mamba run -n $(MAMBA_ENV) git init
	mamba run -n $(MAMBA_ENV) poetry run pre-commit install
	mamba run -n $(MAMBA_ENV) \
		poetry run python -m ipykernel install --user --name=$(PY_KERNEL) --display-name "Python ($(DIR_NAME))"
	@$(MAKE) setup-r
	@echo "All done! You are ready to start coding."

test-py:
	@echo "Running Python tests..."
	mamba run -n $(MAMBA_ENV) poetry run pytest
	@rm -fr .pytest_cache

test-r:
	@echo "Running R tests..."
	mamba run -n $(MAMBA_ENV) \
		Rscript -e "renv::load('$(CURDIR)'); devtools::test('{{cookiecutter.__project_slug}}_rtools')"

test: test-py test-r

docs-r: sync-r
	@echo "Generating R documentation (roxygen2 & pkgdown)..."
	export R_PROFILE_USER; \
		mamba run -n $(MAMBA_ENV) \
		Rscript -e "renv::load('$(CURDIR)'); devtools::document('{{cookiecutter.__project_slug}}_rtools')"; \
		mamba run -n $(MAMBA_ENV) \
		Rscript -e "renv::load('$(CURDIR)'); pkgdown::build_site(override = list(destination = '../docs/r_api'))"

docs-py:
	@echo "Building Sphinx HTML documentation..."
	@mamba run -n $(MAMBA_ENV) \
		poetry export --with docs --without-hashes --format=requirements.txt > docs/requirements.txt
	@mamba run -n $(MAMBA_ENV) \
		poetry run sphinx-build -b html docs docs/_build/html
	@echo "Opening documentation in browser..."
	@mamba run -n $(MAMBA_ENV) \
		poetry run python -c \
		"import webbrowser, os; webbrowser.open('file://' + os.path.realpath('docs/_build/html/index.html'))"

docs: docs-r docs-py
{%- endif %}
