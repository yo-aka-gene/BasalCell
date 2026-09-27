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

# Run Poetry from the Mamba environment while hiding the active Conda
# environment markers from Poetry itself. Without this, Poetry treats
# mamba_{{cookiecutter.__project_slug}} as the active project environment and may install/uninstall
# packages directly in Conda's site-packages.
POETRY = mamba run -n $(MAMBA_ENV) env -u VIRTUAL_ENV -u CONDA_PREFIX -u CONDA_DEFAULT_ENV poetry

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
	mamba_r_lib = (
		Path(os.environ["BASALCELL_MAMBA_PREFIX"]) / "lib" / "R" / "library"
	)
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
{%- if cookiecutter.r_ver != "none" %}
	@export BASALCELL_MAMBA_PREFIX=$$( \
		mamba run -n $(MAMBA_ENV) python -c "import sys; print(sys.prefix)" \
	); \
	$(POETRY) run python -c "$$LAUNCH_JUPYTER_LOGIC"
{%- else %}
	@$(POETRY) run python -c "$$LAUNCH_JUPYTER_LOGIC"
{%- endif %}

clean:
	@echo "Cleaning up built documentation and cache..."
	@rm -rf docs/_build
	@rm -rf .pytest_cache
	@rm -rf .ruff_cache
	@echo "Clean up complete."

bump-patch:
	@$(POETRY) version patch

bump-minor:
	@$(POETRY) version minor

bump-major:
	@$(POETRY) version major

define CALL_PY_FUNC
	$(POETRY) run python -c "import sys; sys.path.append('./.basalcell'); \
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
.PHONY: add-os remove-os lock-conda sync-conda install-conda

add-os:
	@if [ -z "$(strip $(PKG))" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@set -e; \
	set -f; \
	CLEAN_PKG="$(strip $(PKG))"; \
	for pkg in $$CLEAN_PKG; do \
		pkg_name=$$(printf '%s\n' "$$pkg" | sed -E 's/[<>=!~].*$$//'); \
		mamba run -n $(MAMBA_ENV) \
			yq -y -i --arg spec "$$pkg" --arg name "$$pkg_name" \
				'.dependencies |= ( \
					map(select( \
						if type == "string" then \
							(sub("[<>=!~].*$$"; "") != $$name) \
						else \
							true \
						end \
					)) + [$$spec] \
				)' \
				environment.yml; \
	done
	@$(MAKE) lock-conda
	@$(MAKE) sync-conda

remove-os:
	@if [ -z "$(strip $(PKG))" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@set -e; \
	set -f; \
	CLEAN_PKG="$(strip $(PKG))"; \
	for pkg in $$CLEAN_PKG; do \
		pkg_name=$$(printf '%s\n' "$$pkg" | sed -E 's/[<>=!~].*$$//'); \
		mamba run -n $(MAMBA_ENV) \
			yq -y -i --arg name "$$pkg_name" \
				'.dependencies |= map(select( \
					if type == "string" then \
						(sub("[<>=!~].*$$"; "") != $$name) \
					else \
						true \
					end \
				))' \
				environment.yml; \
	done
	@$(MAKE) lock-conda
	@$(MAKE) sync-conda

lock-conda:
	@echo "Generating conda-lock.yml..."
	@TMP_DIR=$$(mktemp -d); \
	trap 'rm -rf "$$TMP_DIR"' EXIT; \
	CONDA_PKGS_DIRS="$$TMP_DIR" \
	mamba run -n base conda-lock \
		-f environment.yml \
		-p osx-arm64 \
		-p linux-64 \
		-p osx-64 \
		--conda conda \
		--lockfile .basalcell/conda-lock.yml

{%- if cookiecutter.r_ver == "none" %}
sync-conda:
	@mamba env update -n $(MAMBA_ENV) -f environment.yml --prune -y

install-conda:
	@echo "Reproducing Mamba environment based on the 'conda-lock.yml' file..."
	mamba run -n base conda-lock install -n $(MAMBA_ENV) .basalcell/conda-lock.yml
{%- else %}
sync-conda:
	@if [ -f .Rprofile ]; then mv .Rprofile .Rprofile_temp_bak; fi
	@if ! mamba env update -n $(MAMBA_ENV) -f environment.yml --prune -y; then \
		if [ -f .Rprofile_temp_bak ]; then mv .Rprofile_temp_bak .Rprofile; fi; \
		exit 1; \
	fi
	@if [ -f .Rprofile_temp_bak ]; then mv .Rprofile_temp_bak .Rprofile; fi

install-conda:
	@echo "Reproducing Mamba environment based on the 'conda-lock.yml' file..."
	@if [ -f .Rprofile ]; then mv .Rprofile .Rprofile_temp_bak; fi
	@if ! mamba run -n base conda-lock install -n $(MAMBA_ENV) .basalcell/conda-lock.yml; then \
		if [ -f .Rprofile_temp_bak ]; then mv .Rprofile_temp_bak .Rprofile; fi; \
		exit 1; \
	fi
	@if [ -f .Rprofile_temp_bak ]; then mv .Rprofile_temp_bak .Rprofile; fi
{%- endif %}

# ==========================================
# Python
# ==========================================
.PHONY: setup-poetry add-py add-pydev remove-py remove-pydev lock-py install-py

CLEAN_PKG_VAL = $(strip $(PKG))

setup-poetry:
	@echo "Configuring Poetry to use a project-local .venv..."
	@$(POETRY) config virtualenvs.create true --local
	@$(POETRY) config virtualenvs.in-project true --local

add-py: setup-poetry
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@$(POETRY) add $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py
	@$(POETRY) export --with dev --without-hashes --format=requirements.txt > .basalcell/requirements.txt

add-pydev: setup-poetry
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@$(POETRY) add --group dev $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py
	@$(POETRY) export --with dev --without-hashes --format=requirements.txt > .basalcell/requirements.txt

remove-py: setup-poetry
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@$(POETRY) remove $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py
	@$(POETRY) export --with dev --without-hashes --format=requirements.txt > .basalcell/requirements.txt

remove-pydev: setup-poetry
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@$(POETRY) remove --group dev $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py
	@$(POETRY) export --with dev --without-hashes --format=requirements.txt > .basalcell/requirements.txt

lock-py: setup-poetry
	@echo "Updating poetry.lock without installing..."
	@$(POETRY) lock
	@$(POETRY) export --with dev --without-hashes --format=requirements.txt > .basalcell/requirements.txt

install-py: setup-poetry
	@echo "Installing Python dependencies from lock file..."
	@$(POETRY) sync --with dev

PYDEV_CORE := ipykernel ipywidgets jupyterlab jupyter-resource-usage \
			  pytest mypy ruff \
			  sphinx sphinx-rtd-theme sphinx-gallery nbsphinx numpydoc myst-parser pandoc \
			  polars pyarrow PyYAML

{%- if cookiecutter.r_ver == "none" %}
# ==========================================
# Advanced Project Management (Python)
# ==========================================
.PHONY: init test docs lock install setup-local terminate purge

init:
	@if ! command -v mamba >/dev/null 2>&1; then \
		echo "mamba is not installed. Please install it first."; \
		exit 1; \
	fi
	$(MAKE) setup-mamba
	@set -e; \
	if [ -f .basalcell/conda-lock.yml ]; then \
		echo "--> Lockfile (.basalcell/conda-lock.yml) found! Delegating to 'make install'..."; \
		$(MAKE) install; \
	else \
		if ! mamba run -n $(MAMBA_ENV) true >/dev/null 2>&1; then \
			mamba env create -n $(MAMBA_ENV) -f environment.yml -y; \
		else \
			echo "Environment $(MAMBA_ENV) already exists. Updating..."; \
			mamba env update -n $(MAMBA_ENV) -f environment.yml --prune -y; \
		fi; \
		mamba run -n $(MAMBA_ENV) bash -c "echo 'python =='$$PYTHON_VERSION > \"\$$CONDA_PREFIX/conda-meta/pinned\""; \
		$(MAKE) add-pydev PKG="$(PYDEV_CORE)"; \
		$(MAKE) setup-local; \
 		$(MAKE) lock; \
	fi
	@echo "All done! You are ready to start coding."

test:
	@$(POETRY) run pytest
	@rm -fr .pytest_cache

docs:
	@echo "Building Sphinx HTML documentation..."
	@$(POETRY) export --with dev --without-hashes --format=requirements.txt > docs/requirements.txt
{%- if cookiecutter.create_package == "true" %}
	@$(POETRY) run sphinx-apidoc -f -o docs/api src/{{cookiecutter.__project_slug}}/
{%- endif %}
	@$(POETRY) run sphinx-apidoc -f -o docs/auxiliary_api {{cookiecutter.__project_slug}}_tools/
	@$(POETRY) run sphinx-build -b html docs docs/_build/html
	@echo "Opening documentation in browser..."
	@$(POETRY) run python -c \
		"import webbrowser, os; webbrowser.open('file://' + os.path.realpath('docs/_build/html/index.html'))"

lock: lock-conda lock-py

install: install-conda
	mamba run -n $(MAMBA_ENV) bash -c "echo 'python =='$$PYTHON_VERSION > \"\$$CONDA_PREFIX/conda-meta/pinned\""
	$(MAKE) install-py
	$(MAKE) setup-local

setup-local: setup-poetry
	@if [ ! -d .git ]; then mamba run -n $(MAMBA_ENV) git init -b main; fi
	mamba run -n $(MAMBA_ENV) pre-commit install
	@$(POETRY) run python -m ipykernel install --user --name=$(PY_KERNEL) --display-name "Python ($(DIR_NAME))"

terminate:
	rm -rf .venv
	mamba env remove -n $(MAMBA_ENV) -y

purge: terminate
	rm -rf .basalcell/conf-lock.yml .basalcell/requirements.txt .basalcell/conda-lock.yml poetry.lock

{%- else %}
# ==========================================
# R
# ==========================================
.PHONY: add-r remove-r lock-r install-r sync-r

define ADD_R_LOGIC
#!/bin/bash
set -e

trap 'mv .Rprofile_proxy_bak .Rprofile_proxy 2>/dev/null || true' EXIT

conda_lib="$$CONDA_PREFIX/lib/R/library"
export RENV_CONFIG_SANDBOX_ENABLED="false"

SUCCESS_PKGS=""
MAMBA_CHANGED=0

try_mamba_install() {
	local channel=$$1
	local prefix=$$2
	local target_pkg="$${prefix}$$3"

	local search_res
	search_res=$$(mamba search -c "$$channel" "^$${target_pkg}$$" 2>/dev/null | grep -v -i "No match" | grep "$${target_pkg}" || true)

	if mamba install --dry-run -q -y -c "$$channel" "$$target_pkg" >/dev/null 2>&1; then
		echo "--> Found $$3 in $$channel. Attempting to install..."

		mv .Rprofile_proxy .Rprofile_proxy_bak 2>/dev/null || true

		if mamba install -y -c "$$channel" "$$target_pkg"; then
			mv .Rprofile_proxy_bak .Rprofile_proxy 2>/dev/null || true
			if ! grep -q -- "- $$target_pkg" environment.yml; then
				yq -y -i ".dependencies += [\"$$target_pkg\"]" environment.yml
				MAMBA_CHANGED=1
			fi
			return 0
		fi
		mv .Rprofile_proxy_bak .Rprofile_proxy 2>/dev/null || true
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

if [ "$$MAMBA_CHANGED" -eq 1 ]; then
	echo "--> Updating Mamba lockfile..."
	$(MAKE) lock-conda
fi

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

define REMOVE_R_LOGIC
#!/bin/bash
set -e
set -f

MAMBA_CHANGED=0
REMOVED_PKGS=""

for pkg in $$CLEAN_PKG; do
	pkg_lower=$$(printf '%s\n' "$$pkg" | tr '[:upper:]' '[:lower:]')

	# Check whether the package is currently Mamba-owned.
	mamba_pkg=$$( \
		yq -r \
			--arg r_name "r-$$pkg_lower" \
			--arg bioc_name "bioconductor-$$pkg_lower" \
			'.dependencies[] \
				| select(type == "string") \
				| sub("[<>=!~].*$$"; "") \
				| select(. == $$r_name or . == $$bioc_name)' \
			environment.yml \
		| head -n 1 \
	)

	if [ -n "$$mamba_pkg" ]; then
		echo "--> Removing $$pkg ($$mamba_pkg) from Mamba dependencies..."

		yq -y -i \
			--arg name "$$mamba_pkg" \
			'.dependencies |= map(select( \
				if type == "string" then \
					(sub("[<>=!~].*$$"; "") != $$name) \
				else \
					true \
				end \
			))' \
			environment.yml

		MAMBA_CHANGED=1
		REMOVED_PKGS="$$REMOVED_PKGS $$pkg"
		continue
	fi

	# Otherwise, check the renv lockfile.
	renv_pkg=$$(python -c '\
import json, sys; \
packages = json.load(open("renv.lock")).get("Packages", {}); \
query = sys.argv[1].lower(); \
print(next((name for name in packages if name.lower() == query), ""))' \
		"$$pkg")

	if [ -n "$$renv_pkg" ]; then
		echo "--> Removing $$renv_pkg from renv..."

		Rscript --vanilla -e '\
			pkg <- commandArgs(trailingOnly = TRUE)[1]; \
			renv::remove(pkg, project = getwd())' \
			"$$renv_pkg"

		REMOVED_PKGS="$$REMOVED_PKGS $$renv_pkg"
	else
		echo "--> [Warning] $$pkg is not managed by Mamba or renv. Skipping."
	fi
done

if [ "$$MAMBA_CHANGED" -eq 1 ]; then
	echo "--> Updating Mamba environment..."
	$(MAKE) lock-conda
	$(MAKE) sync-conda
fi

echo "--> Updating renv.lock..."
Rscript --vanilla -e "renv::snapshot(prompt=FALSE, type='all', force=TRUE)"

if [ -n "$$REMOVED_PKGS" ]; then
	echo "Successfully removed:$$REMOVED_PKGS"
else
	echo "No packages were removed."
fi
endef
export REMOVE_R_LOGIC

remove-r:
	@if [ -z "$(strip $(PKG))" ]; then echo "Error: PKG is not specified. Usage: make remove-r PKG=Seurat"; exit 1; fi
	@export CLEAN_PKG="$(strip $(PKG))"; export MAMBA_ENV="$(MAMBA_ENV)"; \
	mamba run -n $(MAMBA_ENV) bash -c "$$REMOVE_R_LOGIC"

lock-r:
	mamba run -n $(MAMBA_ENV) Rscript --vanilla -e "renv::snapshot(prompt=FALSE, type='all', force=TRUE)"

install-r:
	@TARGETS=$$($(call CALL_PY_FUNC,print_renv_targets)); \
	if [ -z "$$TARGETS" ]; then \
		echo "No renv packages to restore."; \
	else \
		mamba run -n $(MAMBA_ENV) Rscript -e 'pkgs <- commandArgs(trailingOnly = TRUE); renv::restore(packages = pkgs, prompt = FALSE)' $$TARGETS; \
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
.PHONY: init test-py test-r test docs-r docs-py docs lock install setup-local terminate purge

R_PKG_DIR := {{cookiecutter.__project_slug}}_rtools
R_VERSION := {{ cookiecutter.r_ver }}
R_KERNEL_NAME := {{ cookiecutter.__Project_Slug }}

define R_SETUP_INIT_LOGIC
message("--> Initializing new renv environment...")
renv::init(bare = TRUE, bioconductor = TRUE, restart = FALSE)
renv::snapshot(prompt = FALSE, type = "all")
endef
export R_SETUP_INIT_LOGIC

init:
	@if ! command -v mamba >/dev/null 2>&1; then \
		echo "mamba is not installed. Please install it first."; \
		exit 1; \
	fi
	$(MAKE) setup-mamba
	@set -e; \
	if [ -f .basalcell/conda-lock.yml ]; then \
		echo "--> Lockfile (.basalcell/conda-lock.yml) found! Delegating to 'make install'..."; \
		$(MAKE) install; \
	else \
		if ! mamba run -n $(MAMBA_ENV) true >/dev/null 2>&1; then \
			mamba env create -n $(MAMBA_ENV) -f environment.yml -y; \
		else \
			echo "Environment $(MAMBA_ENV) already exists. Updating..."; \
			mamba env update -n $(MAMBA_ENV) -f environment.yml --prune -y; \
		fi; \
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
	@$(POETRY) run pytest
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

docs-py: setup-poetry
	@echo "Building Sphinx HTML documentation..."
	@$(POETRY) export --with dev --without-hashes --format=requirements.txt > docs/requirements.txt
{%- if cookiecutter.create_package == "true" %}
	@$(POETRY) run sphinx-apidoc -f -o docs/api src/{{cookiecutter.__project_slug}}/
{%- endif %}
	@$(POETRY) run sphinx-apidoc -f -o docs/auxiliary_api {{cookiecutter.__project_slug}}_tools/
	@$(POETRY) run sphinx-build -a -E -b html docs docs/_build/html
	@echo "Opening documentation in browser..."
	@$(POETRY) run python -c \
		"import webbrowser, os; webbrowser.open('file://' + os.path.realpath('docs/_build/html/index.html'))"

docs: docs-r docs-py
	@cp -r docs/r_api docs/_build/html/r_api

lock: lock-conda lock-py lock-r

install: install-conda
	mamba run -n $(MAMBA_ENV) bash -c "echo 'python =='$$PYTHON_VERSION > \"\$$CONDA_PREFIX/conda-meta/pinned\""
	@RBASE_VER=$$(mamba list -n $(MAMBA_ENV) "^r-base$$" | awk '/r-base/ {print $$2}'); \
	mamba run -n $(MAMBA_ENV) bash -c "echo 'r-base =='$$RBASE_VER > \"\$$CONDA_PREFIX/conda-meta/pinned\""
	@echo 'R_LIBS_SITE="$${CONDA_PREFIX}/lib/R/library"' > .Renviron
	$(MAKE) install-py
	$(MAKE) install-r
	$(MAKE) setup-local

setup-local: setup-poetry
	@if [ ! -d .git ]; then mamba run -n $(MAMBA_ENV) git init -b main; fi
	mamba run -n $(MAMBA_ENV) pre-commit install
	@$(POETRY) run python -m ipykernel install --user --name=$(PY_KERNEL) --display-name "Python ($(DIR_NAME))"
	mamba run -n $(MAMBA_ENV) Rscript --vanilla -e "\
		Sys.setenv(PATH=paste('$(CURDIR)/.venv/bin', Sys.getenv('PATH'), sep=.Platform[['path.sep']])); \
	    .libPaths(file.path(Sys.getenv('CONDA_PREFIX'), 'lib', 'R', 'library')); \
	    IRkernel::installspec(name='$(R_KERNEL_NAME)_r', displayname='R $(R_VERSION) ($(R_KERNEL_NAME))', user=TRUE)"

terminate:
	rm -rf .venv
	mamba env remove -n $(MAMBA_ENV) -y

purge: terminate
	rm -rf renv/library renv.lock .basalcell/conf-lock.yml .basalcell/requirements.txt .basalcell/conda-lock.yml poetry.lock

{%- endif %}
