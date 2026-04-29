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

RBASE_VER=$(mamba list -n "$MAMBA_ENV" "^r-base$" | awk '/r-base/ {print $2}')
RENV_VER=$(mamba list -n "$MAMBA_ENV" "^r-renv$" | awk '/r-renv/ {print $2}')
IRKERNEL_VER=$(mamba list -n "$MAMBA_ENV" "^r-irkernel$" | awk '/r-irkernel/ {print $2}')

echo "--> Locking Infra: r-base=${RBASE_VER}, r-renv=${RENV_VER}, r-irkernel=${IRKERNEL_VER}"

perl -pi -e "s/- \"?r-base\"?$/- r-base=$RBASE_VER/; \
             s/- \"?r-renv\"?$/- r-renv=$RENV_VER/; \
             s/- \"?r-irkernel\"?$/- r-irkernel=$IRKERNEL_VER/" environment.yml

echo "--> Registering IRkernel..."
poetrt run Rscript --vanilla -e "
    .libPaths(file.path(Sys.getenv('CONDA_PREFIX'), 'lib', 'R', 'library'))
    IRkernel::installspec(
        name='${PROJECT_NAME}_r', 
        displayname='R ${RBASE_VER} (${PROJECT_NAME})', 
        user=TRUE
    )
"

yq -y -i '.dependencies |= map(select(
    type == "!!map" or 
    test("=") or 
    (test("^(r-|bioconductor-)") | not)
))' environment.yml

echo "=== R env setup: Done! ==="
