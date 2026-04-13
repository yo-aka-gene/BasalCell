#!/bin/bash
set -e

R_VERSION="{{ cookiecutter.r_ver }}"

DIR_NAME=$(basename "$PWD")
PROJECT_NAME="${DIR_NAME}_R"

echo "Building R env for ${PROJECT_NAME} (R v${R_VERSION})"
echo "=================================================="

echo "=== 1. rig installation ==="
if ! command -v rig &> /dev/null; then
    echo "rig is not found; trying installation automatically..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # MacOS (Homebrew)
        brew tap r-lib/rig
        brew install --cask rig
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # for Linux (Ubuntu/Debian)
        echo "Installing rig with sudo"
        curl -Ls https://rig.r-lib.org/install.sh | sudo bash
    else
        echo "this OS is unsupported; install rig manually"
        exit 1
    fi
else
    echo "rig is already installed"
fi

echo "=== 2. Setting R version with rig ==="
rig add ${R_VERSION} || echo "Caught rig internal error (likely pak installation), but continuing as R itself should be installed..."

ACTUAL_R_VER=$(rig list | grep -oE "${R_VERSION}[a-zA-Z0-9_.-]*" | head -n 1)

if [ -z "$ACTUAL_R_VER" ]; then
    echo "[ERROR] Failed to find installed R version matching ${R_VERSION}."
    exit 1
fi

echo "Resolved actual R version name: ${ACTUAL_R_VER}"

rig default ${ACTUAL_R_VER}

echo "=== 3. R env restoration with renv ==="
if [ -f "renv.lock" ]; then
    echo "--> Restoring R env according to renv.lock ..."
    Rscript -e "
    if (!requireNamespace('renv', quietly = TRUE)) install.packages('renv')
    renv::restore(prompt = FALSE)
    "
else
    echo "--> renv.lock is not found. Creating a new env"
    Rscript -e "
    options(repos = c(RSPM = 'https://packagemanager.posit.co/cran/latest', CRAN = 'https://cloud.r-project.org'))
    if (!requireNamespace('renv', quietly = TRUE)) install.packages('renv')
    renv::init(bare = TRUE, bioconductor = TRUE)
    install.packages('BiocManager')
    install.packages('IRkernel')
    renv::snapshot(prompt = FALSE)
    "
fi

echo "=== 4. Creating R kernel in Jupyter ==="
poetry run Rscript -e "
IRkernel::installspec(
  name = '${PROJECT_NAME}',
  displayname = 'R ${ACTUAL_R_VER} (${PROJECT_NAME})',
  user = TRUE
)
"

echo "=== R env setup: Done! ==="
