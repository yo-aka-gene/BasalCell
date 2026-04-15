# BasalCell
![version](https://img.shields.io/badge/BasalCell-v.1.0.0-blue.svg?longCache=true)


- Free software: MIT license

BasalCell is a [cookiecutter](https://github.com/cookiecutter/cookiecutter) template designed for reproducible and distributable bioinformatics data analysis. It streamlines the creation of isolated Python and R environments integrated within JupyterLab.

## Features
- **Poetry-managed Python environment**: Pre-configured with `jupyterlab` and essential data science tools.
- **Optional R Integration**: Seamlessly setup an isolated R kernel using `rig` and `renv`.
- **Automated Documentation**: Ready-to-use `Sphinx` configuration (supporting MyST Markdown and Jupyter Notebooks).
- **One-command Workflow**: Setup and launch everything via `make`.

## Usage
### 1. Prerequisites
Ensure you have the `make` command installed:
- **macOS**: `brew install make`
- **Windows**: Use **WSL2** and run `sudo apt update && sudo apt install make`

### 2. Install `cookiecutter`
```bash
pip install -U cookiecutter
```
### 3. Create your project
```bash
cookiecutter git@github.com:yo-aka-gene/BasalCell.git
```

### 4. Setup and Initialization
Answer the prompts to define your project configurations:
- **arguments**:
    - ``project_name``: name your project here
    - ``description``: description for your project
    - ``author_name``: your name (required when `create_package` is `true`)
    - ``email``: your contact info (required when `create_package` is `true`)
    - ``github_username``: your GitHub ID
    - ``python_ver``: the version of Python: choose from `3.10`, `3.11`, or `3.12` (we recommend `3.11` for bioinformatics analyses)
    - `r_ver`: the version of R: choose from `none` (then R setup will be omitted), `4.2`, `4.3`, or `4.4` (we recommend `4.3` for bioinformatics analyses)
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

:warning: in case error codes as follows appear, reboot the terminal:
```
make: poetry: No such file or directory
make: *** [Makefile:25: launch] Error 127
```

## Maintenance
### Add new Python packages
```bash
# For main analysis (e.g., polars, torch, scanpy)
poetry add polars torch scanpy

# For development tools (e.g., flake8)
poetry add -D flake8
```

### **[Optional]** Add new R packages
To add new packages within the isolated `renv` env:
```bash
# Run R within the project context and install
Rscript -e "renv::install('ggplot2')"
```

## Development Tips
### How to upload your project to GitHub
Create a new blank repository on GitHub:
- Repository name: the same as `<your-directory-name>`
- Add README: `OFF`
- Add .gitignore: `No .gitignore`
- Add lisence: `No lisence`

Then, after generating your project, run:
```bash
cd <your-directory-name>
git init
git add .
git commit -m ':tada: Initial commit from BasalCell template'
git remote add origin https://github.com/<your-id>/<project-name>.git
git push -u origin main
```

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
- [Ruff](https://docs.astral.sh/ruff/): Performs linting and automatically reformats your `.py` files. In BasalCell, Ruff is integrated with `pre-commit`, meaning it will automatically run whenever you make a `git commit`.

## Feature(s) to be added in the near future
- Julia kernel
- Executable ipynb
- Linting, unit tests, GitHub Workflow Test for R scripts
- documentation for R scripts (maybe with `myst-parser` and `knitr`?)

## Author(s)
- Yuji Okano
    - GitHub: [@yo-aka-gene](https://github.com/yo-aka-gene)
    - email: [yujiokano@keio.jp](mailto:yujiokano@keio.jp)
---
Open for collaboration! Feel free to open issues or pull requests.
