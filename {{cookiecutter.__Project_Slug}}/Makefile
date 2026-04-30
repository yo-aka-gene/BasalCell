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
add-py:
	@CLEAN_PKG=$$(echo "$(PKG)" | tr "," " " | tr -s " "); \
	mamba run -n $(MAMBA_ENV) \
		poetry add $$CLEAN_PKG
	@$(MAKE) lock-py

add-pydev:
	@CLEAN_PKG=$$(echo "$(PKG)" | tr "," " " | tr -s " "); \
	mamba run -n $(MAMBA_ENV) \
		poetry add --group dev $$CLEAN_PKG
	@$(MAKE) lock-py

remove-py:
	@CLEAN_PKG=$$(echo "$(PKG)" | tr "," " " | tr -s " "); \
	mamba run -n $(MAMBA_ENV) \
		poetry remove $$CLEAN_PKG
	@$(MAKE) lock-py

remove-pydev:
	@CLEAN_PKG=$$(echo "$(PKG)" | tr "," " " | tr -s " "); \
	mamba run -n $(MAMBA_ENV) \
		poetry remove --group dev $$CLEAN_PKG
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
.PHONY: init docs test terminate

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

terminate:
	mamba env remove -n mamba_basalcelldemodev -y

{%- else %}
# ==========================================
# R
# ==========================================
.PHONY: setup-r add-r add-bioc restore-r sync-r

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
	TESTTHAT_VER=$$(mamba list -n $(MAMBA_ENV) "^r-testthat$$" | awk '/r-testthat/ {print $$2}'); \
	STYLER_VER=$$(mamba list -n $(MAMBA_ENV) "^r-styler$$" | awk '/r-styler/ {print $$2}'); \
	LINTR_VER=$$(mamba list -n $(MAMBA_ENV) "^r-lintr$$" | awk '/r-lintr/ {print $$2}'); \
	DEVTOOLS_VER=$$(mamba list -n $(MAMBA_ENV) "^r-devtools$$" | awk '/r-devtools/ {print $$2}'); \
	PKGDOWN_VER=$$(mamba list -n $(MAMBA_ENV) "^r-pkgdown$$" | awk '/r-pkgdown/ {print $$2}'); \
	ROXYGEN_VER=$$(mamba list -n $(MAMBA_ENV) "^r-roxygen2$$" | awk '/r-roxygen2/ {print $$2}'); \
	RMARKDOWN_VER=$$(mamba list -n $(MAMBA_ENV) "^r-rmarkdown$$" | awk '/r-rmarkdown/ {print $$2}'); \
	KNITR_VER=$$(mamba list -n $(MAMBA_ENV) "^r-knitr$$" | awk '/r-knitr/ {print $$2}'); \
	mamba run -n $(MAMBA_ENV) bash -c "echo 'r-base =='$$RBASE_VER > \"\$$CONDA_PREFIX/conda-meta/pinned\""; \
	perl -pi -e "s/- \"?r-base\"?$$/- r-base=$$RBASE_VER/; \
	             s/- \"?r-renv\"?$$/- r-renv=$$RENV_VER/; \
				 s/- \"?r-irkernel\"?$$/- r-irkernel=$$IRKERNEL_VER/; \
				 s/- \"?r-testthat\"?$$/- r-testthat=$$TESTTHAT_VER/; \
				 s/- \"?r-styler\"?$$/- r-styler=$$STYLER_VER/; \
				 s/- \"?r-lintr\"?$$/- r-lintr=$$LINTR_VER/; \
				 s/- \"?r-devtools\"?$$/- r-devtools=$$DEVTOOLS_VER/; \
				 s/- \"?r-pkgdown\"?$$/- r-pkgdown=$$PKGDOWN_VER/; \
				 s/- \"?r-roxygen2\"?$$/- r-roxygen2=$$ROXYGEN2_VER/; \
				 s/- \"?r-rmarkdown\"?$$/- r-rmarkdown=$$RMARKDOWN_VER/; \
	             s/- \"?r-knitr\"?$$/- r-knitr=$$KNITR_VER/" environment.yml; \
	echo "--> Registering IRkernel..."; \
	mamba run -n $(MAMBA_ENV) poetry run Rscript --vanilla -e "\
	    .libPaths(file.path(Sys.getenv('CONDA_PREFIX'), 'lib', 'R', 'library')); \
	    IRkernel::installspec(name='$(R_KERNEL_NAME)_r', displayname='R $$RBASE_VER ($(R_KERNEL_NAME))', user=TRUE)"
	@mamba run -n $(MAMBA_ENV) yq -y -i \
	'.dependencies |= map(select(type == "object" or (type == "string" and (test("=") or (test("^(r-|bioconductor-)") | not)))))' \
	environment.yml
    @echo "=== R env setup: Done! ==="

add-r:
	@mamba run -n $(MAMBA_ENV) bash -c '\
	conda_lib="$$CONDA_PREFIX/lib/R/library"; \
	export RENV_CONFIG_SANDBOX_ENABLED="false"; \
	CLEAN_PKG=$$(echo "$(PKG)" | tr "," " " | tr -s " "); \
	for pkg in $$CLEAN_PKG; do \
		pkg_lower=$$(echo "$$pkg" | tr "[:upper:]" "[:lower:]"); \
		if mamba search -c conda-forge "^r-$$pkg_lower$$" >/dev/null 2>&1; then \
			mamba install -y "r-$$pkg_lower"; \
		elif mamba search -c bioconda "^bioconductor-$$pkg_lower$$" >/dev/null 2>&1; then \
			mamba install -y "bioconductor-$$pkg_lower"; \
		else \
			echo "$$pkg not found in Conda. Falling back to Bioconductor/CRAN via renv..."; \
			Rscript --vanilla -e ".libPaths(\"$$conda_lib\"); options(repos = BiocManager::repositories()); renv::install(\"$$pkg\")"; \
		fi; \
	done; \
	Rscript --vanilla -e ".libPaths(\"$$conda_lib\"); renv::snapshot(prompt=FALSE, type=\"all\", force=TRUE)" \
	'

add-bioc:
	@mamba run -n $(MAMBA_ENV) bash -c '\
	conda_lib="$$CONDA_PREFIX/lib/R/library"; \
	export RENV_CONFIG_SANDBOX_ENABLED="false"; \
	CLEAN_PKG=$$(echo "$(PKG)" | tr "," " " | tr -s " "); \
	for pkg in $$CLEAN_PKG; do \
		pkg_lower=$$(echo "$$pkg" | tr "[:upper:]" "[:lower:]"); \
		if mamba search -c bioconda "^bioconductor-$$pkg_lower$$" >/dev/null 2>&1; then \
			mamba install -y "bioconductor-$$pkg_lower"; \
		else \
			echo "$$pkg not found in Conda. Falling back to Bioconductor/CRAN via renv..."; \
			Rscript --vanilla -e ".libPaths(\"$$conda_lib\"); options(repos = BiocManager::repositories()); renv::install(\"$$pkg\")"; \
		fi; \
	done; \
	Rscript --vanilla -e ".libPaths(\"$$conda_lib\"); renv::snapshot(prompt=FALSE, type=\"all\", force=TRUE)" \
	'

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

R_PROFILE_USER := $(DIR_NAME)/.Rprofile

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

terminate:
	mamba env remove -n mamba_basalcelldemodev -y
	rm -rf renv/library

{%- endif %}
