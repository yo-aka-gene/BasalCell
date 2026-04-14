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
    - ``author_name``: your name
    - ``email``: your contact info
    - ``github_username``: your GitHub ID
    - ``python_ver``: the version of Python: choose from `3.10`, `3.11`, or `3.12` (we recommend `3.11` for bioinformatics analyses)
    - `r_ver`: the version of R: choose from `none` (then R setup will be omitted), `4.2`, `4.3`, or `4.4` (we recommend `4.3` for bioinformatics analyses)
    - `create_package`: choose `true` if you will publish your project as a Python package; otherwise `false`

Once you've answered the prompts, the initialization script (`make init`) will automatically run to set up your environments.

### 5. Launch Jupyter Lab
Navigate to your project directory and run:
```bash
cd <your-project-slug>
make launch
```
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

### Other Contents (v.1.0.0)
1. README file
    - appropriate README file (depending on your project configuration) will be generated
    - default README file includes a default image as follows;
    <div align="center">
    <img src="./{{cookiecutter.__Project_Slug}}/docs/_static/default_logo.png" alt="graphical abstract" width="300" height="300" title="graphical abstract">
    </div>

    - you can replace the image as you like (e.g., graphical abstract for your research article)
2. documentation
    - Documentation is powered by `Sphinx`. To build the HTML version:
    ```bash
    make docs
    ```
    The output will be generated in `docs/_build/html/`.

## Feature(s) to be added in the near future
- Julia kernel
- Executable ipynb
- GitHub Workflow Test for R scripts

## Author(s)
- Yuji Okano
    - GitHub: [@yo-aka-gene](https://github.com/yo-aka-gene)
    - email: [yujiokano@keio.jp](mailto:yujiokano@keio.jp)
---
Open for collaboration! Feel free to open issues or pull requests.
