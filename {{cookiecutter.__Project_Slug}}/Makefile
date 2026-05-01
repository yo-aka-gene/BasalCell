# ==========================================
# Basic Project Management
# ==========================================
.PHONY: launch clean bump-patch bump-minor bump-major

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
            "--IdentityProvider.token=basalcelldemodev",
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
                    url = f"{url}?token=basalcelldemodev"

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

# ==========================================
# Mamba
# ==========================================
.PHONY: add-os sync-os

add-os:
	@CLEAN_PKG=$$(echo "$(PKG)" | tr "," " " | tr -s " "); \
	mamba run -n $(MAMBA_ENV) \
		yq -y -i '.dependencies |= (. + ("'"$$CLEAN_PKG"'" | split(" ")) | unique)' environment.yml
	mamba env update -n $(MAMBA_ENV) -f environment.yml --prune

sync-os:
	mamba env update -n $(MAMBA_ENV) -f environment.yml --prune

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

add-pydev:
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@mamba run -n $(MAMBA_ENV) poetry add --group dev $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py

remove-py:
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@mamba run -n $(MAMBA_ENV) poetry remove $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py

remove-pydev:
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified."; exit 1; fi
	@mamba run -n $(MAMBA_ENV) poetry remove --group dev $(CLEAN_PKG_VAL)
	@$(MAKE) lock-py

lock-py:
	@echo "Updating poetry.lock without installing..."
	mamba run -n $(MAMBA_ENV) poetry lock

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
.PHONY: init docs test terminate

init:
	@echo "Starting project environment setup..."
	@if ! command -v mamba >/dev/null 2>&1; then \
		echo "mamba is not installed. Please install it first."; \
		exit 1; \
	fi
	@if [ ! -d "$$(mamba info --base)/envs/$(MAMBA_ENV)" ]; then \
		mamba env create -f environment.yml -y; \
	else \
		echo "Environment $(MAMBA_ENV) already exists. Updating..."; \
		mamba env update -f environment.yml --prune -y; \
	fi
	mamba run -n $(MAMBA_ENV) poetry config virtualenvs.create false
	mamba run -n $(MAMBA_ENV) bash -c "echo 'python =='$$PYTHON_VERSION > \"\$$CONDA_PREFIX/conda-meta/pinned\""
	@$(MAKE) add-pydev PKG="$(PYDEV_CORE)"
	mamba run -n $(MAMBA_ENV) poetry install
	mamba run -n $(MAMBA_ENV) git init -b main
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

terminate:
	mamba env remove -n mamba_basalcelldemodev -y

{%- else %}
# ==========================================
# R
# ==========================================
.PHONY: setup-r add-r pin-r restore-r sync-r

R_VERSION := {{ cookiecutter.r_ver }}
R_KERNEL_NAME := {{ cookiecutter.__Project_Slug }}

define R_SETUP_COMMON_LOGIC
conda_lib <- file.path(Sys.getenv("CONDA_PREFIX"), "lib", "R", "library")
.libPaths(conda_lib)
sysname <- Sys.info()[["sysname"]]
if (sysname == "Linux") {
    options(repos = c(CRAN = "https://packagemanager.posit.co/cran/__linux__/jammy/latest"), pkgType = "source")
} else {
    options(repos = c(CRAN = "https://cloud.r-project.org"), pkgType = "source")
}
endef
export R_SETUP_COMMON_LOGIC

define R_SETUP_INIT_LOGIC
message("--> Initializing new renv environment...")
renv::init(bare = TRUE, bioconductor = TRUE, restart = FALSE)
renv::snapshot(prompt = FALSE, type = "all")
endef
export R_SETUP_INIT_LOGIC

setup-r:
	@echo "Building R env for $(R_KERNEL_NAME)..."
	@echo "=================================================="
	@echo 'R_LIBS_SITE="$${CONDA_PREFIX}/lib/R/library"' > .Renviron
	@export R_LIBS_USER=""; export R_LIBS_SITE=""; \
	mamba run -n $(MAMBA_ENV) Rscript --vanilla -e "$$R_SETUP_COMMON_LOGIC"
	@if [ ! -f renv.lock ]; then \
		mamba run -n $(MAMBA_ENV) Rscript --vanilla -e "$$R_SETUP_INIT_LOGIC"; \
	else \
		echo "--> renv.lock found. Delegating to 'make restore-r'..."; \
		$(MAKE) restore-r; \
	fi
	@RBASE_VER=$$(mamba list -n $(MAMBA_ENV) "^r-base$$" | awk '/r-base/ {print $$2}'); \
	RENV_VER=$$(mamba list -n $(MAMBA_ENV) "^r-renv$$" | awk '/r-renv/ {print $$2}'); \
	IRKERNEL_VER=$$(mamba list -n $(MAMBA_ENV) "^r-irkernel$$" | awk '/r-irkernel/ {print $$2}'); \
	mamba run -n $(MAMBA_ENV) bash -c "echo 'r-base =='$$RBASE_VER > \"\$$CONDA_PREFIX/conda-meta/pinned\""; \
	perl -pi -e "s/- \"?r-base\"?$$/- r-base=$$RBASE_VER/; \
	             s/- \"?r-renv\"?$$/- r-renv=$$RENV_VER/; \
				 s/- \"?r-irkernel\"?$$/- r-irkernel=$$IRKERNEL_VER/" environment.yml; \
	mamba run -n $(MAMBA_ENV) poetry run Rscript --vanilla -e "\
	    .libPaths(file.path(Sys.getenv('CONDA_PREFIX'), 'lib', 'R', 'library')); \
	    IRkernel::installspec(name='$(R_KERNEL_NAME)_r', displayname='R $$RBASE_VER ($(R_KERNEL_NAME))', user=TRUE)"
	@echo "=== R env setup: Done! ==="


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


define PIN_R_LOGIC
#!/bin/bash
set -e

search_and_pin() {
	local prefix=$$1
	local pkg_name="$${prefix}$$2"

	local version
	version=$$(mamba list -n "$$MAMBA_ENV" "^$${pkg_name}$$" | grep -v '^#' | grep "$${pkg_name}" | awk '{print $$2}')

	if [ -n "$$version" ]; then
		echo "--> Successfully pinned: $$pkg_name == $$version!"

		if ! grep -q "^ *- $${pkg_name}" environment.yml; then
			yq -y -i ".dependencies += [\"$${pkg_name}=$$version\"]" environment.yml
		else
			perl -pi -e "s/^(\s*-\s*\"?)$${pkg_name}(\"?[=>~]?.*)$$/\1$${pkg_name}=$$version/" environment.yml
		fi

		mkdir -p "$$CONDA_PREFIX/conda-meta"
		if ! grep -q "^$${pkg_name}[ =]" "$$CONDA_PREFIX/conda-meta/pinned" 2>/dev/null; then
			echo "$${pkg_name} ==$$version" >> "$$CONDA_PREFIX/conda-meta/pinned"
		else
			perl -pi -e "s/^$${pkg_name}[ =].*$$/$${pkg_name} ==$$version/" "$$CONDA_PREFIX/conda-meta/pinned"
		fi

		return 0
	fi
	return 1
}

PKG_LOWER=$$1

if search_and_pin "r-" "$$PKG_LOWER"; then
	exit 0
elif search_and_pin "bioconductor-" "$$PKG_LOWER"; then
	exit 0
else
	exit 1
fi
endef
export PIN_R_LOGIC

pin-r:
	@if [ -z "$(PKG)" ]; then echo "Error: PKG is not specified. Usage: make pin-r PKG=seurat"; exit 1; fi
	@for pkg in $(CLEAN_PKG_VAL); do \
		pkg_lower=$$(echo "$$pkg" | tr "[:upper:]" "[:lower:]"); \
		echo "------------------------------------------------------------"; \
		echo "Processing $$pkg..."; \
		if mamba run -n $(MAMBA_ENV) bash -c "$$PIN_R_LOGIC" _ "$$pkg_lower"; then \
			continue; \
		else \
			echo "--> $$pkg is not installed yet. Calling add-r to install it first..."; \
			$(MAKE) add-r PKG="$$pkg"; \
			mamba run -n $(MAMBA_ENV) bash -c "$$PIN_R_LOGIC" _ "$$pkg_lower" || true; \
		fi; \
	done
	@echo "Pinning complete!"
	@echo "Packages that were never installed were automatically added."
	@echo "Note: Packages falling back to renv (CRAN/Bioc) are not managed by Mamba and cannot be pinned..."


define RESTORE_R_LOGIC
import json
import os
import subprocess
import sys

def main():
    lockfile = "renv.lock"
    if not os.path.exists(lockfile):
        print(
            "ERROR: renv.lock not found. Please run environment initialization first."
        )
        sys.exit(1)

    print("Analyzing renv.lock for Mamba restoration...")
    with open(lockfile, "r") as f:
        lock_data = json.load(f)

    packages = lock_data.get("Packages", {})
    mamba_targets = []
    renv_fallbacks = []

    for pkg_name, pkg_info in packages.items():
        source = pkg_info.get("Source", "")
        version = pkg_info.get("Version", "")

        if source == "Bioconductor":
            conda_name = f"bioconductor-{pkg_name.lower()}"
        elif source in ["Repository", "CRAN"]:
            conda_name = f"r-{pkg_name.lower()}"
        else:
            renv_fallbacks.append(pkg_name)
            continue

        conda_spec = f"{conda_name}={version}"
    
        result = subprocess.run(
            ["mamba", "search", conda_spec],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if result.returncode == 0:
            mamba_targets.append(conda_spec)
        else:
            print(f"{conda_spec} not found in Conda. Assigning to renv...")
            renv_fallbacks.append(pkg_name)

    if mamba_targets:
        print(f"Installing {len(mamba_targets)} packages via Mamba...")
        try:
            subprocess.run(["mamba", "install", "-y"] + mamba_targets, check=True)
        except subprocess.CalledProcessError:
            print(
                "ERROR: Mamba installation failed. Check your network or environment."
            )
            sys.exit(1)
    else:
        print("No exact matches found in Mamba.")

    print(
        f"Running renv::restore() for the final sync ({len(renv_fallbacks)}"
        " packages left to renv)..."
    )

    conda_lib = os.path.join(os.environ.get("CONDA_PREFIX", ""), "lib", "R", "library")
    r_cmd = f".libPaths('{conda_lib}'); "
    "Sys.setenv(RENV_CONFIG_SANDBOX_ENABLED='false'); renv::restore(prompt=FALSE)"

    try:
        subprocess.run(["Rscript", "--vanilla", "-e", r_cmd], check=True)
    except subprocess.CalledProcessError:
        print("ERROR: renv::restore() failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
endef
export RESTORE_R_LOGIC


restore-r:
	@echo "Restoring R environment from renv.lock..."
	@echo "$$RESTORE_R_LOGIC" | mamba run -n $(MAMBA_ENV) python3 -
# 	mamba run -n $(MAMBA_ENV) python restore_r_env.py

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
.PHONY: init test-py test-r test docs-r docs-py docs terminate

R_PKG_DIR := {{cookiecutter.__project_slug}}_rtools

init:
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
	mamba run -n $(MAMBA_ENV) bash -c "echo 'python =='$$PYTHON_VERSION > \"\$$CONDA_PREFIX/conda-meta/pinned\""
	@$(MAKE) add-pydev PKG="$(PYDEV_CORE)"
	mamba run -n $(MAMBA_ENV) poetry install
	mamba run -n $(MAMBA_ENV) git init -b main
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
		poetry export --with docs --without-hashes --format=requirements.txt > docs/requirements.txt
	@mamba run -n $(MAMBA_ENV) \
		poetry run sphinx-build -b html docs docs/_build/html
	@echo "Opening documentation in browser..."
	@mamba run -n $(MAMBA_ENV) \
		poetry run python -c \
		"import webbrowser, os; webbrowser.open('file://' + os.path.realpath('docs/_build/html/index.html'))"

docs: docs-r docs-py

terminate:
	mamba env remove -n mamba_basalcelldemodev -y
	rm -rf renv/library

{%- endif %}
