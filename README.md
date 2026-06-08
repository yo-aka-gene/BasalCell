<h1 align="center">
<img src=https://github.com/yo-aka-gene/BasalCell/blob/main/logo/basalcell_logo_long.svg?raw=true width="500">
</h1><br>


![BasalCell Version](https://img.shields.io/github/v/tag/yo-aka-gene/BasalCell?label=BasalCell&color=blue)
[<img src="https://img.shields.io/badge/DOI-10.64898/2026.05.27.720396-FAB70C?style=flat&logo=doi">](https://doi.org/10.64898/2026.05.27.720396)


- Free software: MIT license

BasalCell is a [cookiecutter](https://github.com/cookiecutter/cookiecutter) template designed for reproducible and distributable bioinformatics data analysis. It streamlines the creation of isolated Python and R environments integrated within JupyterLab.

**:eyes: See it in action:** Check out the [BasalCellDemo repository](https://github.com/yo-aka-gene/BasalCellDemo) for a complete scRNA-seq workflow example.

### Citation
```
@article{okano2026basalcell,
  title={BasalCell: A project scaffold generator for bioinformatics analysis},
  author={Okano, Yuji and Ishikawa, Tetsuo and Sakurada, Kazuhiro},
  journal={bioRxiv},
  pages={2026--05},
  year={2026},
  publisher={Cold Spring Harbor Laboratory}
}
```

## Features
- **Poetry-managed Python environment**: Pre-configured with `jupyterlab` and essential data science tools.
- **Optional R Integration**: Seamlessly setup an isolated R kernel using `renv`.
- **Automated Documentation**: Ready-to-use `Sphinx` configuration (supporting MyST Markdown and Jupyter Notebooks).
- **One-command Workflow**: Setup and launch everything via `make`.

## Usage
### 1. Prerequisites
Before using BasalCell, ensure you have the following installed on your system:
- `Miniforge` (This automatically provides `Python` and `pip`)
- `make`
- `git`

**For macOS**

Using [Homebrew](https://brew.sh/) is the easiest way:
```bash
brew install miniforge make git
conda init zsh
```

**For Windows (WSL2 / Ubuntu)**

Run the following command to install all the prerequisites at once:
```bash
sudo apt update && sudo apt install -y make git
```
Then, install Miniforge by downloading the official installer:
```bash
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
bash Miniforge3-Linux-x86_64.sh -b -p $HOME/miniforge3
source $HOME/miniforge3/bin/activate
conda init bash

```

### 2. Install `cookiecutter`
```bash
pip install -U cookiecutter
```
### 3. Create your project
```bash
cookiecutter git@github.com:yo-aka-gene/BasalCell.git
```
> :bulb: **Note for GitHub authentication**: Alternatively, you can install via HTTPS instead of SSH:
> ```bash
> cookiecutter https://github.com/yo-aka-gene/BasalCell.git
> ```

### 4. Setup and Initialization
Answer the prompts to define your project configurations:
- **arguments**:
    - ``project_name``: name your project here
    - ``description``: description for your project
    - ``author_name``: your name (required when `create_package` is `true`)
    - ``email``: your contact info (required when `create_package` is `true`)
    - ``github_username``: your GitHub ID
    - ``python_ver``: the version of Python: choose from `3.12`, or `3.13`.
    - `r_ver`: the version of R: choose from `none` (then R setup will be omitted), `4.3`, or `4.4`.
    - `create_package`: choose `true` if you will publish your project as a Python package; otherwise `false`

Once you've answered the prompts, the initialization script (`make init`) will automatically run to set up your environments.

### 5. Launch Jupyter Lab
Navigate to your project directory and run:
```bash
cd <your-directory-name>
make launch
```
Then `Jupyter Lab` will pop up in your default browser.
Default token will be your project slug:
e.g., `Your Project Name` -> `your_project_name`

## Maintenance
### Add new Python packages
```bash
# For main analysis (e.g., polars, torch, scanpy)
make add-py PKG=polars
make add-py PKG="torch scanpy<1.12"

# For development tools (e.g., tqdm)
make add-pydev PKG=tqdm
```

:warning: Do not add packages via `pip install` or `poetry add`.
These commands are invalid for adding designated packages in the BasalCell env.

### **[Optional]** Add new R packages
To add new packages within the isolated `renv` env:
```bash
# For R packages (e.g., ggplot2, dplyr, Seurat, DESeq2, org.Hs.eg.db)
make add-r PKG="ggplot2 dplyr Seurat DESeq2 org.Hs.eg.db"

# Sometimes R packages require OS-level dependencies (e.g., perl)
# If so, you can add them to the Mamba env with add-os
make add-os PKG=perl
```

:warning: Do not add packages via `install.packages`, `renv::install`,  or `apt-get`.
These commands are invalid for adding designated packages in the BasalCell env.

## Development Tips
### How to upload your project to GitHub
Create a new blank repository on GitHub:
- Repository name: the same as `<your-directory-name>`
- Add README: `OFF`
- Add .gitignore: `No .gitignore`
- Add license: `No license`

Then, after generating your project, run:
```bash
cd <your-directory-name>
git add .
git commit -m ':tada: Initial commit from BasalCell template'
git remote add origin https://github.com/<your-id>/<project-name>.git
git push -u origin main
```
**Note**: During `make init`, `git init` has already executed.

### Documentation
Documentation is a cornerstone of the readability of your analysis code. Utilize the following frameworks to create your own documentation:
- [Sphinx](https://www.sphinx-doc.org/en/master/): A widely used framework for Python code documentation. BasalCell comes with a built-in system that allows you to easily write documentation in `.md` format and build it into HTML. Please refer to `docs/index.md` inside the generated project for syntax examples.
- [docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html): If you create custom modules in directories like `tools` within the generated project, or if you publish your project as a package, adding docstrings to your functions and classes will allow Sphinx to automatically build documentation for them. BasalCell supports the NumPy style by default.
- [Read the Docs](https://about.readthedocs.com/): Hosts and publishes documentation directly from your GitHub repository. While BasalCell comes pre-configured with the basic settings, you will need to create a Read the Docs account, link it to your GitHub account, and import your repository to actually publish the documentation.

Once you are ready to build your documentation, run:
```bash
cd <your-directory-name>
make docs
```
This allows you to preview the documentation in your local environment. The output will be generated in `docs/_build/html/`.
The HTML files that will actually be published are automatically generated on the server when you push to the `main` branch.

As a placeholder for the `README.md` and documentation icon, the following image is inserted by default:

<div align="center">
<img src="./{{cookiecutter.__Project_Slug}}/docs/_static/default_logo.png" alt="graphical abstract" width="300" height="300" title="graphical abstract">
</div>

Please create your own icon image or graphical abstract and replace it accordingly.

### Test and Readability Improvement
Writing test code is crucial for verifying the behavior of your developed code. Additionally, linting is essential to improve code readability. BasalCell makes it easy to run tests and linters by utilizing the following frameworks:
- [Pytest](https://docs.pytest.org/en/stable/): The standard testing library for Python. Please refer to the official documentation on how to write test code, and place your tests in the appropriate paths within the `tests` directory of your generated project.
- [Ruff](https://docs.astral.sh/ruff/): Performs linting and automatically reformats your `.py` files. In BasalCell, Ruff is integrated with [`pre-commit`](https://pre-commit.com/), meaning it will automatically run whenever you make a `git commit`.
- [GitHub Actions](https://github.com/features/actions): A CI/CD platform. BasalCell is pre-configured to automatically run the aforementioned workflows on the server whenever a `pull request` is created or `git push origin main` is executed, ensuring code quality and reproducibility even during collaborative data analysis.

### **[Optional]**: Integration of R env
- Usage: select `r_ver` and an R kernel will be set in your Jupyter Lab env.
- Analysis: run analysis codes in R using `.ipynb` files and the R kernel in Jupyter Lab.
- Documentation: While `nbsphinx` handles your Jupyter Notebooks, BasalCell uses [`pkgdown`](https://pkgdown.r-lib.org/) to automatically generate a dedicated reference website for your custom R functions. Simply document your functions using standard [`roxygen2`](https://roxygen2.r-lib.org/) comments, and this R API site is seamlessly integrated and accessible directly from the main Sphinx documentation. When creating R-related documentation, make sure to run `make docs` locally and commit the generated HTML files to the GitHub repository.
- Test: use [`testthat`](https://testthat.r-lib.org/) package. `testthat.R` and test directory for R `testthat/` are all set in `tests` inside your project directory.
- Linting: `pre-commit` automatically runs linting using [`lintr`](https://lintr.r-lib.org/) and [`styler`](https://styler.r-lib.org/).
- CI/CD: GitHub Actions are also implemented for R language as well.

### Instructions for Make Commands
- BasalCell utilizes `GNU Make` to streamline complex CLI operations into simple one-liners. Please perform fundamental operations via the `make` commands listed below.

#### common
| command | run when... | description |
| :---: | :----: | :----|
| `init` | initializing environments | This command is automatically triggered in `cookiecutter git@github.com:yo-aka-gene/BasalCell.git`. Run this command when you reboot the environment after `make terminate` or when your cloned a repository based on BasalCell. |
| `launch` | launching Jupyter Lab |  This connects `Jupyter Lab` and your default browser. Sometimes access token will be asked: the default token will be your project slug (e.g., `Your Project-ABC` -> `your_project_abc`)|
| `lock` | before `git commit` | This transcribes the environment configuration ensuring reproducibility. **Always run this command after you added/removed packages before `git commit` to reflect the alteration in GitHub** |
| `dump-all` | exporting all version configurations as a matrix (after `make lock`) | This exports version configurations of all packages (including Python, R, and System dependencies) as a matrix in the designated data format. Run `make dump-all` to have a `csv` file. For alternative file formats, `ipc`, `feather`, `pq`, and `parquet` are supported (designate them like `make dump-all EXT=pq`). |
| `dump-core` | exporting core version configurations as a matrix (after `make lock`) | This exports version configurations of core packages (non-development Python and R packages) as a matrix in the designated data format. Run `make dump-core` to have a `csv` file. For alternative file formats, `ipc`, `feather`, `pq`, and `parquet` are supported (designate them like `make dump-core EXT=pq`). |
| `dump` | exporting queried version configurations as a matrix (after `make lock`) | This exports version configurations of queried packages as a matrix in the designated data format (e.g., `make dump KEYS='numpy DESeq2' EXT=pq`). |
| `report` | exporting version configurations as a human-readable `.md` file (after `make lock`) | This exports version configurations of queried packages as a `md` file. Pass `KEYS=all`, `KEYS=core`, or `KEYS=<query>` (e.g., `make report KEYS='numpy DESeq2'`) to get necessary information. |
| `install` | copying existing enviroment | This command is automatically triggered in `make init` for cloned repositories. This reproduces locked environments. |
| `test` | unit test | This command is triggers unit test modules defined via `pytest` (test code deposited in `tests/`), `doctest` (`Examples` in docstrings), or `testthat` (test code deposited in `<your_project_name>_rtools/tests/testthat/`)  if available |
| `docs` | building documentations | This command builds documentation HTML files with `Sphinx` or `pkgdown`. Created HTML files will pop in your default browser. |
| `terminate` | deprecating existing environment | Run `make terminate init` to restart the environment (e.g., when you got stuck with certain errors). |


#### Python
| command | run when... | description |
| :---: | :----: | :----|
| `add-py` | adding python package(s) | e.g., `make add-py PKG='scanpy pandas numpy'` |
| `add-pydev` | adding python package(s) for development | e.g., `make add-pydev PKG=watchdog` |
| `remove-py` | removing python package(s) | e.g., `make remove-py PKG='scanpy pandas numpy'` |
| `remove-pydev` | removing python package(s) for development | e.g., `make remove-pydev PKG=watchdog` |


#### R
| command | run when... | description |
| :---: | :----: | :----|
| `add-r` | adding R package(s) | e.g., `make add-r PKG='ggplot2 dplyr Seurat DESeq2 org.Hs.eg.db'` |

#### System dependencies
| command | run when... | description |
| :---: | :----: | :----|
| `add-os` | adding OS software(s) | e.g., `make add-os PKG='cmake cxx-compiler'` **Note**: OS dependencies for Python/R packages are automatically installed via `add-py`, `add-pydev`, or `add-r`  |

#### For Developers
| command | run when... | description |
| :---: | :----: | :----|
| `bump-patch` | before `git version patch` | A shortcurt for `mamba run <mamba_env> poetry version patch` |
| `bump-minor` | before `git version minor` | A shortcurt for `mamba run <mamba_env> poetry version minor` |
| `bump-major` | before `git version major` | A shortcurt for `mamba run <mamba_env> poetry version major` |


## Feature(s) to be added in the near future
- Julia kernel
- Executable ipynb

## Author(s)
- Yuji Okano
    - GitHub: [@yo-aka-gene](https://github.com/yo-aka-gene)
    - email: [yujiokano@keio.jp](mailto:yujiokano@keio.jp)
---
Open for collaboration! Feel free to open issues or pull requests.
