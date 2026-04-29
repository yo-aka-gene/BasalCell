#!/bin/bash
set -e

R_VERSION="{{ cookiecutter.r_ver }}"
MAMBA_ENV="mamba_{{cookiecutter.__project_slug}}"
DIR_NAME=$(basename "$PWD")
PROJECT_NAME="${DIR_NAME}_R"

echo "Building R env for ${PROJECT_NAME} (in ${MAMBA_ENV})"
echo "=================================================="

export R_LIBS_USER=""

if [ -f "renv.lock" ]; then
    echo "--> Restoring R env according to renv.lock ..."
    Rscript -e "
    sysname <- Sys.info()[['sysname']]
    conda_prefix <- Sys.getenv('CONDA_PREFIX')

    if (sysname == 'Linux') {
        Sys.setenv(LDFLAGS = paste0('-L', conda_prefix, '/lib -Wl,-rpath,', conda_prefix, '/lib'))
        Sys.setenv(CPPFLAGS = paste0('-I', conda_prefix, '/include'))
        Sys.setenv(PKG_CONFIG_PATH = paste0(conda_prefix, '/lib/pkgconfig'))
        options(repos = c(CRAN = 'https://packagemanager.posit.co/cran/__linux__/jammy/latest'))
        options(pkgType = 'binary')
    } else {
        options(repos = c(CRAN = 'https://packagemanager.posit.co/cran/latest'))
        options(pkgType = 'source')
    }

    if (!requireNamespace('pak', quietly = TRUE)) install.packages('pak', repos = 'https://cloud.r-project.org', type = getOption('pkgType'))
    if (!requireNamespace('renv', quietly = TRUE)) install.packages('renv', repos = 'https://cloud.r-project.org', type = getOption('pkgType'))
    renv::restore(prompt = FALSE)
    "
else
    echo "--> renv.lock is not found. Creating a new env"
    Rscript -e "
    sysname <- Sys.info()[['sysname']]
    conda_prefix <- Sys.getenv('CONDA_PREFIX')

    if (sysname == 'Linux') {
        Sys.setenv(LDFLAGS = paste0('-L', conda_prefix, '/lib -Wl,-rpath,', conda_prefix, '/lib'))
        Sys.setenv(CPPFLAGS = paste0('-I', conda_prefix, '/include'))
        Sys.setenv(PKG_CONFIG_PATH = paste0(conda_prefix, '/lib/pkgconfig'))
        cran_url <- 'https://packagemanager.posit.co/cran/__linux__/jammy/latest'
        pkg_type <- 'binary'
    } else {
        cran_url <- 'https://packagemanager.posit.co/cran/latest'
        pkg_type <- 'source'
    }
    options(repos = c(CRAN = cran_url))
    options(pkgType = pkg_type)
    if (!requireNamespace('pak', quietly = TRUE)) install.packages('pak', repos = 'https://cloud.r-project.org', type = getOption('pkgType'))
    if (!requireNamespace('renv', quietly = TRUE)) install.packages('renv', repos = 'https://cloud.r-project.org', type = getOption('pkgType'))
    renv::init(bare = TRUE, bioconductor = TRUE)
    "
    Rscript -e "
    renv::install(c(
        'testthat',
        'styler',
        'lintr',
        'BiocManager',
        'IRkernel',
        'devtools', 
        'pkgdown', 
        'roxygen2',
        'rmarkdown',
        'knitr'
    ))
    renv::snapshot(prompt = FALSE, type = 'all')
    "
fi

echo "--> Registering IRkernel to Jupyter..."
poetry run Rscript -e "
IRkernel::installspec(
  name = '${PROJECT_NAME}',
  displayname = 'R ${R_VERSION} (${PROJECT_NAME})',
  user = TRUE
)
"

echo "=== R env setup: Done! ==="
