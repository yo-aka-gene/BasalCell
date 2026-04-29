#!/bin/bash
set -e

R_VERSION="{{ cookiecutter.r_ver }}"
MAMBA_ENV="mamba_{{cookiecutter.__project_slug}}"
DIR_NAME=$(basename "$PWD")
PROJECT_NAME="${DIR_NAME}_R"

echo "Building R env for ${PROJECT_NAME}..."
echo "=================================================="

export R_LIBS_USER=""
export R_LIBS_SITE=""

Rscript --vanilla -e "
    conda_lib <- file.path(Sys.getenv('CONDA_PREFIX'), 'lib', 'R', 'library')
    .libPaths(conda_lib)

    sysname <- Sys.info()[['sysname']]
    if (sysname == 'Linux') {
        options(repos = c(CRAN = 'https://packagemanager.posit.co/cran/__linux__/jammy/latest'), pkgType = 'source')
    } else {
        options(repos = c(CRAN = 'https://cloud.r-project.org'), pkgType = 'source')
    }

    if (!file.exists('renv.lock')) {
        message('--> Initializing new renv environment...')
        renv::init(bare = TRUE, bioconductor = TRUE, restart = FALSE)
        renv::snapshot(prompt = FALSE, type = 'all')
    } else {
        message('--> Restoring from renv.lock...')
        renv::restore(prompt = FALSE)
    }
"

echo "--> Registering IRkernel..."
poetry run Rscript --vanilla -e ".libPaths(file.path(Sys.getenv('CONDA_PREFIX'), 'lib', 'R', 'library')); IRkernel::installspec(name='${PROJECT_NAME}', displayname='R ${R_VERSION} (${PROJECT_NAME})', user=TRUE)"

echo "=== R env setup: Done! ==="
poetry run yq -y -i '.dependencies |= map(select(
    type == "!!map" or 
    test("=") or 
    (test("^(r-|bioconductor-)") | not)
))' environment.yml
