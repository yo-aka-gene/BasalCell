#!/bin/bash
set -e

R_VERSION="{{ cookiecutter.r_ver }}"
MAMBA_ENV="mamba_{{cookiecutter.__project_slug}}"
DIR_NAME=$(basename "$PWD")
PROJECT_NAME="${DIR_NAME}_R"

echo "Building R env for ${PROJECT_NAME} (in ${MAMBA_ENV})"
echo "=================================================="
if [ -f "renv.lock" ]; then
    echo "--> Restoring R env according to renv.lock ..."
    Rscript -e "
    if (!requireNamespace('renv', quietly = TRUE)) install.packages('renv')
    renv::restore(prompt = FALSE)
    "
else
    echo "--> renv.lock is not found. Creating a new env"
    Rscript -e "
    options(repos = c(
        RSPM = 'https://packagemanager.posit.co/cran/__linux__/noble/latest', 
        CRAN = 'https://cloud.r-project.org'
    ))
    if (!requireNamespace('renv', quietly = TRUE)) install.packages('renv')
    renv::init(bare = TRUE, bioconductor = TRUE)
    renv::install(c(
        'testthat',
        'styler',
        'lintr',
        'BiocManager',
        'IRkernel',
        'devtools', 
        'pkgdown', 
        'roxygen2'
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
