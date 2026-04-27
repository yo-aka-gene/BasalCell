<h1 align="center">
<img src=https://github.com/yo-aka-gene/BasalCell/blob/main/logo/basalcell_logo_long.svg?raw=true width="500">
</h1><br>


![BasalCell Version](https://img.shields.io/github/v/tag/yo-aka-gene/BasalCell?label=BasalCell&color=blue)


- Free software: MIT license

BasalCell is a [cookiecutter](https://github.com/cookiecutter/cookiecutter) template designed for reproducible and distributable bioinformatics data analysis. It streamlines the creation of isolated Python and R environments integrated within JupyterLab.

**:eyes: See it in action:** Check out the [BasalCellDemo repository](https://github.com/yo-aka-gene/BasalCellDemo) for a complete scRNA-seq workflow example.

## Features
- **Poetry-managed Python environment**: Pre-configured with `jupyterlab` and essential data science tools.
- **Optional R Integration**: Seamlessly setup an isolated R kernel using `renv`.
- **Automated Documentation**: Ready-to-use `Sphinx` configuration (supporting MyST Markdown and Jupyter Notebooks).
- **One-command Workflow**: Setup and launch everything via `make`.

## Usage
### 1. Prerequisites
Before using BasalCell, ensure you have the following installed on your system:
- `Python` (3.10–3.12)
- `pip`
- `miniconda`
- `make`

**For macOS**

Using [Homebrew](https://brew.sh/) is the easiest way:
```bash
brew install miniconda make
```
> :bulb: **Python Installation Tip**: We highly recommend using `pyenv` (`brew install pyenv`) to manage Python versions cleanly. Alternatively, for a quick setup, you can install Python directly `brew install` (e.g.,  `brew install python@3.12`).

**For Windows (WSL2 / Ubuntu)**

Run the following command to install all the prerequisites at once:
```bash
sudo apt update && sudo apt install -y miniconda make python3 python3-pip
```
> :bulb: **Python Installation Tip**: While the command above installs the system Python, setting up `pyenv` is considered a best practice in bioinformatics to prevent conflicts with the OS environment.

### 2. Install `cookiecutter`
```bash
pip install -U cookiecutter
```
### 3. Create your project
```bash
cookiecutter https://github.com/yo-aka-gene/BasalCell.git
```
> :bulb: **Note for GitHub authentication**: If you have set up SSH keys for GitHub, you can run the following code instead:
> ```bash
> cookiecutter git@github.com:yo-aka-gene/BasalCell.git
> ```

### 4. Setup and Initialization
Answer the prompts to define your project configurations:
- **arguments**:
    - ``project_name``: name your project here
    - ``description``: description for your project
    - ``author_name``: your name (required when `create_package` is `true`)
    - ``email``: your contact info (required when `create_package` is `true`)
    - ``github_username``: your GitHub ID
    - ``python_ver``: the version of Python: choose from `3.10`, `3.11`, or `3.12`.
    - `r_ver`: the version of R: choose from `none` (then R setup will be omitted), `4.2`, `4.3`, `4.4`, or `4.5`.
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
make add-py PKG='torch "scanpy<1.12"'

# For development tools (e.g., tqdm)
make add-pydev PKG=tqdm
```

### **[Optional]** Add new R packages
To add new packages within the isolated `renv` env:
```bash
# For R packages (e.g., ggplot2)
make add-r PKG=ggplot2

# For R packages from Bioconductor (e.g., DESeq2, edgeRp)
make add-bioc PKG="DESeq2 edgeR"

# Sometimes R packages requires OS-level dependencies (e.g., perl)
# If so, you can add them to the Conda env with add-os
make add-os PKG=perl
```

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
- Documentation: `nbsphinx` will handle your R analysis codes. If you need to show your `.R` scripts, create a `.md` file in `docs` and reference your R scripts as follows:
````
```{literalinclude} ../tools/example.R
:language: r
:linenos: true
```
````
- Test: use [`testthat`](https://testthat.r-lib.org/) package. `testthat.R` and test directory for R `testthat/` are all set in `tests` inside your project directory.
- Linting: `pre-commit` automatically runs linting using [`lintr`](https://lintr.r-lib.org/) and [`styler`](https://styler.r-lib.org/).
- CI/CD: GitHub Actions are also implemented for R language as well.


## Feature(s) to be added in the near future
- Julia kernel
- Executable ipynb

## Author(s)
- Yuji Okano
    - GitHub: [@yo-aka-gene](https://github.com/yo-aka-gene)
    - email: [yujiokano@keio.jp](mailto:yujiokano@keio.jp)
---
Open for collaboration! Feel free to open issues or pull requests.
