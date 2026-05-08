# ==========================================
# Mamba Setup for BasalCell
# ==========================================
.PHONY: setup-mamba

setup-mamba:
	@echo "Installing 'conda-lock' to 'base' environment..."
	mamba install -n base -c conda-forge conda-lock yq -y

# ==========================================
# Basic Project Management
# ==========================================
.PHONY: launch clean bump-patch bump-minor bump-major dump-all dump-core dump report

MAMBA_ENV := mamba_{{cookiecutter.__project_slug}}
DIR_NAME := $(shell basename $(CURDIR))
PY_KERNEL := $(DIR_NAME)_py
VERSION := $(shell grep '^version = ' pyproject.toml | cut -d '"' -f 2)
PYTHON_VERSION := {{cookiecutter.python_ver}}

define LAUNCH_JUPYTER_LOGIC
import os
import platform
from pathlib import Path
import textwrap
import subprocess
import sys
import webbrowser


def open_browser(url):
    is_wsl = "microsoft" in platform.uname().release.lower()

    if is_wsl:
        try:
            subprocess.run(["wslview", url], check=True)
        except FileNotFoundError:
            safe_url = url.replace("&", "^&")
            subprocess.run(["cmd.exe", "/c", "start", safe_url])
    else:
        webbrowser.open(url)

def start_jupyter():
    print("Initiating Jupyter Lab")

    process = subprocess.Popen(
        [
            "jupyter", "lab",
            "--no-browser",
            "--port=8888",
            "--ip=0.0.0.0",
            "--allow-root",
            "--IdentityProvider.token={{cookiecutter.__project_slug}}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    browser_opened = False

    try:
        for line in process.stdout:
            sys.stdout.write(line)

            if "http://127.0.0.1" in line and "/lab" in line and not browser_opened:
                url = line.strip().split(" ")[-1]

                if "token=" not in url:
                    url = f"{url}?token={{cookiecutter.__project_slug}}"

                print("\n" + "=" * 70)
                print("Jupyter Lab is available at:")
                print(f"\033[1;36m{url}\033[0m")
                print("=" * 70 + "\n")

                print("Connecting to Jupyter Lab via default browser...")
                try:
                    open_browser(url)
                except Exception as e:
                    print("Failed to open browser automatically.")
                    print(f"Reason: {e}")
                    print("\nPlease open the URL below manually:")
                    print(f"\n    \033[1;36m{url}\033[0m\n")

                browser_opened = True

    except KeyboardInterrupt:
        print("Terminating Jupyter Lab")
        process.terminate()
        process.wait()
        print("Jupyter Lab has terminated")

if __name__ == "__main__":
{%- if cookiecutter.r_ver != "none" %}
{% raw %}
	project_root = Path.cwd()
	mamba_r_lib = Path(sys.prefix) / "lib" / "R" / "library"
	r_profile_proxy = project_root / ".Rprofile_proxy"
	r_profile_content = textwrap.dedent(f"""\
		old_wd <- getwd()
		setwd('{project_root.as_posix()}')

		source('renv/activate.R')

		mamba_lib <- '{mamba_r_lib.as_posix()}'
		if (dir.exists(mamba_lib)) {{
			.libPaths(c(.libPaths(), mamba_lib))
		}}

		setwd(old_wd)
	""")
	r_profile_proxy.write_text(r_profile_content)
	os.environ["R_PROFILE_USER"] = str(r_profile_proxy)
	try:
		start_jupyter()
	finally:
		r_profile_proxy.unlink(missing_ok=True)
{% endraw %}
{%- else %}
	start_jupyter()
{%- endif %}
endef
export LAUNCH_JUPYTER_LOGIC


launch:
	@mamba run -n $(MAMBA_ENV) \
		poetry run python -c "$$LAUNCH_JUPYTER_LOGIC"

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

define CALL_PY_FUNC
	mamba run -n $(MAMBA_ENV) python -c "import sys; sys.path.append('./.basalcell'); \
	from basalcell_system import $(1); \
	args = [arg for arg in '$(2)'.split() if arg]; \
	$(1)(*args)"
endef
export CALL_PY_FUNC

dump-all:
	@echo "Exporting all dependencies..."
	@$(call CALL_PY_FUNC,export_all_dependencies,$(EXT))

dump-core:
	@echo "Exporting essential packages..."
	@$(call CALL_PY_FUNC,export_essentials,$(EXT))

dump:
	@echo "Exporting queried packages..."
	@$(call CALL_PY_FUNC,export,$(KEYS) $(EXT))

report:
	@echo "Generating human-readable dependency report..."
	@$(call CALL_PY_FUNC,report,$(KEYS))

# ==========================================
# Mamba
# ==========================================
.PHONY: add-os sync-os lock-conda install-conda

add-os:
	@CLEAN_PKG=$$(echo "$(PKG)" | tr "," " " | tr -s " "); \
	mamba run -n $(MAMBA_ENV) \
		yq -y -i '.dependencies |= (. + ("'"$$CLEAN_PKG"'" | split(" ")) | unique)' environment.yml
	mamba env update -n $(MAMBA_ENV) -f environment.yml --prune

sync-os:
	mamba env update -n $(MAMBA_ENV) -f environment.yml --prune

lock-conda:
	@echo "Generating conda-lock.yml..."
	mamba clean --all --yes
	CONDA_PKGS_DIRS=$$(mktemp -d) conda-lock -f environment.yml -p osx-arm64 -p linux-64 -p osx-64 --conda conda --lockfile .basalcell/conda-lock.yml

install-conda:
	@echo "Reproducing Mamba environment based on the 'conda-lock.yml' file..."
	conda-lock install -n $(MAMBA_ENV) .basalcell/conda-lock.yml

# ==========================================
# Python
# ==========================================
.PHONY: add-py add-pydev remove-py remove-pydev lock-py install-py

COMMA := ,
CLEAN_PKG_VAL = $(strip $(subst $(COMMA), ,$(PKG)))

add-py:
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@mamba run -n $(MAMBA_ENV) poetry add $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py
	@mamba run -n $(MAMBA_ENV) \
		poetry export --with dev --without-hashes --format=requirements.txt > .basalcell/requirements.txt

add-pydev:
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@mamba run -n $(MAMBA_ENV) poetry add --group dev $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py
	@mamba run -n $(MAMBA_ENV) \
		poetry export --with dev --without-hashes --format=requirements.txt > .basalcell/requirements.txt

remove-py:
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@mamba run -n $(MAMBA_ENV) poetry remove $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py
	@mamba run -n $(MAMBA_ENV) \
		poetry export --with dev --without-hashes --format=requirements.txt > .basalcell/requirements.txt

remove-pydev:
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@mamba run -n $(MAMBA_ENV) poetry remove --group dev $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py
	@mamba run -n $(MAMBA_ENV) \
		poetry export --with dev --without-hashes --format=requirements.txt > .basalcell/requirements.txt

lock-py:
	@echo "Updating poetry.lock without installing..."
	mamba run -n $(MAMBA_ENV) poetry lock
	@mamba run -n $(MAMBA_ENV) \
		poetry export --with dev --without-hashes --format=requirements.txt > .basalcell/requirements.txt

install-py:
	@echo "Installing Python dependencies from lock file..."
	mamba run -n $(MAMBA_ENV) poetry install

PYDEV_CORE := ipykernel ipywidgets jupyterlab jupyter-resource-usage \
			  pytest mypy ruff pre-commit \
			  sphinx sphinx-rtd-theme sphinx-gallery nbsphinx numpydoc myst-parser pandoc \
			  polars pyarrow PyYAML

{%- if cookiecutter.r_ver == "none" %}
# ==========================================
# Advanced Project Management (Python)
# ==========================================
.PHONY: init test docs lock install setup-local terminate

init:
	@if ! command -v mamba >/dev/null 2>&1; then \
		echo "mamba is not installed. Please install it first."; \
		exit 1; \
	fi
	$(MAKE) setup-mamba
	@if [ -f .basalcell/conda-lock.yml ]; then \
		echo "--> Lockfile (.basalcell/conda-lock.yml) found! Delegating to 'make install'..."; \
		$(MAKE) install; \
	else \
		if ! mamba env list | grep -q $(MAMBA_ENV); then \
			mamba env create -f environment.yml -y; \
		else \
			echo "Environment $(MAMBA_ENV) already exists. Updating..."; \
			mamba env update -f environment.yml --prune -y; \
		fi; \
		mamba run -n $(MAMBA_ENV) poetry config virtualenvs.create false; \
		mamba run -n $(MAMBA_ENV) bash -c "echo 'python =='$$PYTHON_VERSION > \"\$$CONDA_PREFIX/conda-meta/pinned\""; \
		$(MAKE) add-pydev PKG="$(PYDEV_CORE)"; \
		$(MAKE) setup-local; \
 		$(MAKE) lock; \
	fi
	@echo "All done! You are ready to start coding."

test:
	mamba run -n $(MAMBA_ENV) poetry run pytest
	@rm -fr .pytest_cache

docs:
	@echo "Building Sphinx HTML documentation..."
	@mamba run -n $(MAMBA_ENV) \
		poetry export --with dev --without-hashes --format=requirements.txt > docs/requirements.txt
{%- if cookiecutter.create_package == "true" %}
	@mamba run -n $(MAMBA_ENV) \
		poetry run sphinx-apidoc -f -o docs/api src/{{cookiecutter.__project_slug}}/
{%- endif %}
	@mamba run -n $(MAMBA_ENV) \
		poetry run sphinx-apidoc -f -o docs/auxiliary_api {{cookiecutter.__project_slug}}_tools/
	@mamba run -n $(MAMBA_ENV) \
		poetry run sphinx-build -b html docs docs/_build/html
	@echo "Opening documentation in browser..."
	@mamba run -n $(MAMBA_ENV) \
		poetry run python -c \
		"import webbrowser, os; webbrowser.open('file://' + os.path.realpath('docs/_build/html/index.html'))"

lock: lock-conda lock-py

install: install-conda
	mamba run -n $(MAMBA_ENV) poetry config virtualenvs.create false
	mamba run -n $(MAMBA_ENV) bash -c "echo 'python =='$$PYTHON_VERSION > \"\$$CONDA_PREFIX/conda-meta/pinned\""
	$(MAKE) install-py
	$(MAKE) setup-local

setup-local:
	@if [ ! -d .git ]; then mamba run -n $(MAMBA_ENV) git init -b main; fi
	mamba run -n $(MAMBA_ENV) poetry run pre-commit install
	mamba run -n $(MAMBA_ENV) \
		poetry run python -m ipykernel install --user --name=$(PY_KERNEL) --display-name "Python ($(DIR_NAME))"

terminate:
	mamba env remove -n $(MAMBA_ENV) -y
	rm -rf .basalcell/conf-lock.yml .basalcell/requirements.txt poetry.lock

{%- else %}
# ==========================================
# R
# ==========================================
.PHONY: add-r lock-r install-r sync-r

define ADD_R_LOGIC
#!/bin/bash
set -e
conda_lib="$$CONDA_PREFIX/lib/R/library"
export RENV_CONFIG_SANDBOX_ENABLED="false"

SUCCESS_PKGS=""

try_mamba_install() {
	local channel=$$1
	local prefix=$$2
	local target_pkg="$${prefix}$$3"

	local search_res
	search_res=$$(mamba search -c "$$channel" "^$${target_pkg}$$" 2>/dev/null | grep -v -i "No match" | grep "$${target_pkg}" || true)

	if mamba install --dry-run -q -y -c "$$channel" "$$target_pkg" >/dev/null 2>&1; then
		echo "--> Found $$3 in $$channel. Attempting to install..."

		if mamba install -y -c "$$channel" "$$target_pkg"; then
			if ! grep -q -- "- $$target_pkg" environment.yml; then
				yq -y -i ".dependencies += [\"$$target_pkg\"]" environment.yml
			fi
			return 0
		fi
	fi
	return 1
}

for pkg in $$CLEAN_PKG; do
	pkg_lower=$$(echo "$$pkg" | tr "[:upper:]" "[:lower:]")

	if try_mamba_install "conda-forge" "r-" "$$pkg_lower"; then
		SUCCESS_PKGS="$$SUCCESS_PKGS $$pkg"
	elif try_mamba_install "bioconda" "bioconductor-" "$$pkg_lower"; then
		SUCCESS_PKGS="$$SUCCESS_PKGS $$pkg"
	else
		echo "--> $$pkg not found or failed in Conda. Falling back to Bioconductor/CRAN via renv..."
		if Rscript --vanilla -e ".libPaths(\"$$conda_lib\"); options(repos = BiocManager::repositories()); renv::install(\"$$pkg\")"; then
			SUCCESS_PKGS="$$SUCCESS_PKGS $$pkg"
		else
			echo "--> [Error] Completely failed to install $$pkg via all methods. Skipping."
		fi
	fi
done

echo "--> Updating renv.lock..."
Rscript --vanilla -e ".libPaths(\"$$conda_lib\"); renv::snapshot(prompt=FALSE, type='all', force=TRUE)"

if [ -n "$$SUCCESS_PKGS" ]; then
	echo "Successfully added:$$SUCCESS_PKGS"
else
	echo "No packages were successfully installed."
fi
endef
export ADD_R_LOGIC

add-r:
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified. Usage: make add-r PKG=seurat"; exit 1; fi
	@export CLEAN_PKG="$(CLEAN_PKG_VAL)"; export MAMBA_ENV="$(MAMBA_ENV)"; \
	mamba run -n $(MAMBA_ENV) bash -c "$$ADD_R_LOGIC"

lock-r:
	mamba run -n $(MAMBA_ENV) Rscript --vanilla -e "renv::snapshot(prompt=FALSE, type='all', force=TRUE)"

install-r:
	@TARGETS=$$($(call CALL_PY_FUNC,print_renv_targets)); \
	if [ -z "$$TARGETS" ]; then \
		echo "No renv packages to restore."; \
	else \
		mamba run -n $(MAMBA_ENV) Rscript -e '\
			pkgs <- commandArgs(trailingOnly = TRUE); \
			renv::restore(packages = pkgs, prompt = FALSE) \
		' $$TARGETS; \
	fi

PROJECT_NAME := $(shell grep '^name = ' pyproject.toml | cut -d '"' -f 2)
DESCRIPTION_STR := $(shell grep '^description = ' pyproject.toml | cut -d '"' -f 2)

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
.PHONY: init test-py test-r test docs-r docs-py docs lock install setup-local terminate

R_PKG_DIR := {{cookiecutter.__project_slug}}_rtools
R_VERSION := {{ cookiecutter.r_ver }}
R_KERNEL_NAME := {{ cookiecutter.__Project_Slug }}

define R_SETUP_INIT_LOGIC
message("--> Initializing new renv environment...")
renv::init(bare = TRUE, bioconductor = TRUE, restart = FALSE)
renv::snapshot(prompt = FALSE, type = "all")
endef
export R_SETUP_INIT_LOGIC

init: setup-mamba
	@if ! command -v mamba >/dev/null 2>&1; then \
		echo "mamba is not installed. Please install it first."; \
		exit 1; \
	fi
	$(MAKE) setup-mamba
	@if [ -f .basalcell/conda-lock.yml ]; then \
		echo "--> Lockfile (.basalcell/conda-lock.yml) found! Delegating to 'make install'..."; \
		$(MAKE) install; \
	else \
		if ! mamba env list | grep -q $(MAMBA_ENV); then \
			mamba env create -f environment.yml -y; \
		else \
			echo "Environment $(MAMBA_ENV) already exists. Updating..."; \
			mamba env update -f environment.yml --prune -y; \
		fi; \
		mamba run -n $(MAMBA_ENV) poetry config virtualenvs.create false; \
		mamba run -n $(MAMBA_ENV) bash -c "echo 'python =='$$PYTHON_VERSION > \"\$$CONDA_PREFIX/conda-meta/pinned\""; \
		RBASE_VER=$$(mamba list -n $(MAMBA_ENV) "^r-base$$" | awk '/r-base/ {print $$2}'); \
		RENV_VER=$$(mamba list -n $(MAMBA_ENV) "^r-renv$$" | awk '/r-renv/ {print $$2}'); \
		IRKERNEL_VER=$$(mamba list -n $(MAMBA_ENV) "^r-irkernel$$" | awk '/r-irkernel/ {print $$2}'); \
		mamba run -n $(MAMBA_ENV) bash -c "echo 'r-base =='$$RBASE_VER > \"\$$CONDA_PREFIX/conda-meta/pinned\""; \
		perl -pi -e "s/- \"?r-base\"?$$/- r-base=$$RBASE_VER/; \
					 s/- \"?r-renv\"?$$/- r-renv=$$RENV_VER/; \
					 s/- \"?r-irkernel\"?$$/- r-irkernel=$$IRKERNEL_VER/" environment.yml; \
		$(MAKE) add-pydev PKG="$(PYDEV_CORE)"; \
		echo 'R_LIBS_SITE="$${CONDA_PREFIX}/lib/R/library"' > .Renviron; \
		mamba run -n $(MAMBA_ENV) Rscript --vanilla -e "$$R_SETUP_INIT_LOGIC"; \
		$(MAKE) setup-local; \
 		$(MAKE) lock; \
	fi
	@echo "All done! You are ready to start coding."

test-py:
	@echo "Running Python tests..."
	mamba run -n $(MAMBA_ENV) poetry run pytest
	@rm -fr .pytest_cache

test-r:
	@echo "Running R tests..."
	@mamba run -n $(MAMBA_ENV) \
		Rscript -e " \
		Sys.setenv(RENV_CONFIG_SYNCHRONIZED_CHECK='false'); \
		renv::load('$(CURDIR)'); \
		.libPaths(c(.libPaths(), file.path(Sys.getenv('CONDA_PREFIX'), 'lib', 'R', 'library'))); \
		Sys.setenv(R_LIBS = paste(.libPaths(), collapse = .Platform[['path.sep']])); \
		devtools::test('$(R_PKG_DIR)')"

test: test-py test-r

docs-r: sync-r
	@echo "Generating R documentation (roxygen2 & pkgdown)..."
	@rm -rf ./docs/r_api docs/_build/html/r_api
	@mamba run -n $(MAMBA_ENV) \
		Rscript -e " \
		Sys.setenv(RENV_CONFIG_SYNCHRONIZED_CHECK='false'); \
		renv::load('$(CURDIR)'); \
		.libPaths(c(.libPaths(), file.path(Sys.getenv('CONDA_PREFIX'), 'lib', 'R', 'library'))); \
		devtools::document('$(R_PKG_DIR)'); \
		pkgdown::build_site(pkg = '$(R_PKG_DIR)', override = list(destination = '../docs/r_api'), new_process = FALSE, install = FALSE)"

docs-py:
	@echo "Building Sphinx HTML documentation..."
	@mamba run -n $(MAMBA_ENV) \
		poetry export --with dev --without-hashes --format=requirements.txt > docs/requirements.txt
{%- if cookiecutter.create_package == "true" %}
	@mamba run -n $(MAMBA_ENV) \
		poetry run sphinx-apidoc -f -o docs/api src/{{cookiecutter.__project_slug}}/
{%- endif %}
	@mamba run -n $(MAMBA_ENV) \
		poetry run sphinx-apidoc -f -o docs/auxiliary_api {{cookiecutter.__project_slug}}_tools/
	@mamba run -n $(MAMBA_ENV) \
		poetry run sphinx-build -a -E -b html docs docs/_build/html
	@echo "Opening documentation in browser..."
	@mamba run -n $(MAMBA_ENV) \
		poetry run python -c \
		"import webbrowser, os; webbrowser.open('file://' + os.path.realpath('docs/_build/html/index.html'))"

docs: docs-r docs-py
	@cp -r docs/r_api docs/_build/html/r_api

lock: lock-conda lock-py lock-r

install: install-conda
	mamba run -n $(MAMBA_ENV) poetry config virtualenvs.create false
	mamba run -n $(MAMBA_ENV) bash -c "echo 'python =='$$PYTHON_VERSION > \"\$$CONDA_PREFIX/conda-meta/pinned\""
	@RBASE_VER=$$(mamba list -n $(MAMBA_ENV) "^r-base$$" | awk '/r-base/ {print $$2}'); \
	mamba run -n $(MAMBA_ENV) bash -c "echo 'r-base =='$$RBASE_VER > \"\$$CONDA_PREFIX/conda-meta/pinned\""
	@echo 'R_LIBS_SITE="$${CONDA_PREFIX}/lib/R/library"' > .Renviron
	$(MAKE) install-py
	$(MAKE) install-r
	$(MAKE) setup-local

setup-local:
	@if [ ! -d .git ]; then mamba run -n $(MAMBA_ENV) git init -b main; fi
	mamba run -n $(MAMBA_ENV) poetry run pre-commit install
	mamba run -n $(MAMBA_ENV) \
		poetry run python -m ipykernel install --user --name=$(PY_KERNEL) --display-name "Python ($(DIR_NAME))"
	mamba run -n $(MAMBA_ENV) poetry run Rscript --vanilla -e "\
	    .libPaths(file.path(Sys.getenv('CONDA_PREFIX'), 'lib', 'R', 'library')); \
	    IRkernel::installspec(name='$(R_KERNEL_NAME)_r', displayname='R $(R_VERSION) ($(R_KERNEL_NAME))', user=TRUE)"

terminate:
	mamba env remove -n $(MAMBA_ENV) -y
	rm -rf renv/library renv.lock .basalcell/conf-lock.yml .basalcell/requirements.txt poetry.lock

{%- endif %}
