#!/bin/bash
set -e

R_VERSION="{{ cookiecutter.r_ver }}"

DIR_NAME=$(basename "$PWD")
PROJECT_NAME="${DIR_NAME}_R"

echo "Building R env for ${PROJECT_NAME} (R v${R_VERSION})"
echo "=================================================="

echo "=== 0. Checking OS dependencies ==="
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get &> /dev/null; then
        echo "Ubuntu/Debian/WSL detected. Installing essential C libraries for R packages..."
        echo "Administrator privileges might be required. Please enter your sudo password."
        sudo -v
        sudo apt-get update -y
        sudo apt-get install -y libxml2-dev libcurl4-openssl-dev libssl-dev libzmq3-dev libuv1-dev libglpk-dev
    else
        echo "[WARNING] apt-get not found. Please ensure essential C libraries are installed manually."
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected. Skipping OS-level dependency installation."
fi

echo "=== 1. rig installation ==="
if ! command -v rig &> /dev/null; then
    echo "rig is not found; trying installation automatically..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # MacOS (Homebrew)
        brew tap r-lib/rig
        brew install --cask rig
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # for Linux (Ubuntu/Debian)
        echo "Administrator privileges are required for Linux/WSL environments. Please enter your sudo password."
        sudo -v
        echo "Downloading rig directly from GitHub releases..."
        curl -kLs "https://github.com/r-lib/rig/releases/download/latest/rig-linux-latest.tar.gz" | sudo tar -xz -C /usr/local
        hash -r
        if ! command -v rig &> /dev/null; then
            echo "[ERROR] Automated installation of rig failed."
            echo "Please download the binary manually and place it in /usr/local/bin."
            exit 1
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Git Bash (Windows native)
        echo "[ERROR] Windows native environment (Git Bash) detected."
        echo "Please open PowerShell as Administrator and run the following command:"
        echo "      winget install -e --id RProject.rig"
        echo "After installation, restart this terminal and run 'make init' again."
        exit 1
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
    renv::install(c(
        'testthat',
        'styler',
        'lintr',
        'BiocManager',
        'IRkernel'
    ))
    renv::snapshot(prompt = FALSE, type = 'all')
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
