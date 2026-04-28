# {{cookiecutter.project_name}}
[![DOI](https://img.shields.io/badge/DOI-wip-blue.svg?longCache=true)]()
[![PMID](https://img.shields.io/badge/PMID-wip-orange.svg?longCache=true)]()
<div align="center">
<img src="./docs/_static/default_logo.png" alt="graphical abstract" width="300" height="300" title="graphical abstract">
</div>

{%- if cookiecutter.description != "" %}
{{cookiecutter.description}}
{%- endif %}

## Project Summary
1. Write
2. Down
3. What
4. You
5. Did
6. Here

## Copyright of Data
***describe the copyright and licensing of your dataset(s)***

### Data Installation
***describe how to install your dataset(s)***

## Project Directory Tree
```bash
{{cookiecutter.__project_slug}}/
    ├── .github/
    │   ├── workflows/
    │   │   └── test.yml                        # write CI/CD configuration here
    │   └── pull_request_template.md
{% if cookiecutter.r_ver != "none" %}    ├── {{cookiecutter.__project_slug}}_rtools/{% endif %}
{% if cookiecutter.r_ver != "none" %}    │   ├── R/                                 # write your R scripts here{% endif %}
{% if cookiecutter.r_ver != "none" %}    │   ├── tests/{% endif %}
{% if cookiecutter.r_ver != "none" %}    │   │   ├── testthat/                      # write your R test code here{% endif %}
{% if cookiecutter.r_ver != "none" %}    │   │   └── testthat.R{% endif %}
{% if cookiecutter.r_ver != "none" %}    │   └── vignettes/                         # write your R vignettes here (not actively recommended){% endif %}
{% if cookiecutter.r_ver != "none" %}    │   │   └── example.Rmd{% endif %}
{% if cookiecutter.r_ver != "none" %}    │   ├── _pkgdown.yml                       # write R documentation configuration here{% endif %}
{% if cookiecutter.r_ver != "none" %}    │   └── DESCRIPTION                        # write R API info (semi-auto generated){% endif %}
    ├── {{cookiecutter.__project_slug}}_tools/
    │   └── __init__.py                         # init file for your Python utility scripts for analysis                     
    ├── data/                                   # store your data here
    ├── docs/                                   # documentation
    │   ├── _static/                            # directory for image files etc.
    │   │   └── default_logo.png                # place holder image for docs
    │   ├── jupyternb/                          # write .ipynb files here
    │   │   ├── output                          # export analysis results here
    │   │   ├── data                            # symbolic link to ../../data
    │   │   └── tools                           # symbolic link to ../../tools
    │   ├── conf.py                             # documentation configuration
    │   └── index.md                            # draft for index page
{% if cookiecutter.r_ver != "none" %}    ├── renv/                                   # R env configuration{% endif %}
{% if cookiecutter.create_package == "true" %}    ├── src/{% endif %}
{% if cookiecutter.create_package == "true" %}    │   └── {{cookiecutter.__project_slug}}/{% endif %}
{% if cookiecutter.create_package == "true" %}    │       └── __init__.py                     # init file for your Python package{% endif %}
    ├── test/                                   # write your Python test code here
    ├── .gitignore
    ├── .pre-commit-config.yaml                 # configuration for linting and tests
    ├── Makefile                                # shortcut commands
    ├── launch_jupyter.py                       # helper func for starting Jupyter
    ├── poetry.lock                             # detailed Python env configuration
    ├── pyproject.toml                          # declarative Python env configuration
{% if cookiecutter.r_ver != "none" %}    ├── renv.lock                               # detailed R env configuration{% endif %}
{% if cookiecutter.r_ver != "none" %}    ├── setup_r_env.sh                          # helper func for R env setup{% endif %}
    └── README.md                               # this file
```

## Author(s)
- {{cookiecutter.author_name}} <[{{cookiecutter.email}}](mailto:{{cookiecutter.email}})>
    - GitHub account: [{{cookiecutter.github_username}}](https://github.com/{{cookiecutter.github_username}})


## Guidance for Collaborators and Researchers trying to reproduce the results
### :warning: Prerequisites
- This repository was created based on the [`BasalCell`](https://github.com/yo-aka-gene/BasalCell) template (version {{cookiecutter.__version}}); please follow the `README.md` documentation for the prerequisite setup
- **For Windows Users**: Please make sure to access this directory via `WSL`


### Setting the Virtual Env
1. Fork this repository and clone it to your local environment
2.  Run the initialization command:
```bash
make init
```
{% set use_r = cookiecutter.r_ver != 'none' -%}
{% if use_r %}
(This command will automatically install Python dependencies, register the Jupyter kernel, and build the R virtual environment).
{% else %}
(This command will automatically install Python dependencies and register the Jupyter kernel).
{% endif %}

### Launching Jupyter Lab
Run:
```bash
make launch
```

### Adding Packages
This project uses a unified interface to add dependencies:
- **Python**: `make add-py PKG=name` (or `add-pydev` for dev tools)
    - overwrite `poetry.lock` with `make lock-py`
    - install dependencies listed in `poetry.lock` with `make install-py`
- **R**: `make add-r PKG=name` (or `add-bioc` for Bioconductor)
- **OS**: `make add-os PKG=name` (for mamba/system libraries)

### Building Documentation
- For a brief guide on how to write documentation across various file types, please refer to the README.md of the [`BasalCell`](https://github.com/yo-aka-gene/BasalCell) repository.
{% if cookiecutter.r_ver != "none" %}- When creating R-related documentation, make sure to run `make docs` locally and commit the generated HTML files to the GitHub repository.{% endif %}


### Update Version Tags
```bash
make bump-patch  # 0.1.0 -> 0.1.1
make bump-minor  # 0.1.1 -> 0.2.0
make bump-major  # 0.2.0 -> 1.0.0
```

### Further Guidance for Repository Management
- Refer to the [`BasalCell`](https://github.com/yo-aka-gene/BasalCell) repository for detailed descriptions
- Refer to the [`BasalCellDemo`](https://github.com/yo-aka-gene/BasalCellDemo) repository for a real-world example of scRNA-seq data analysis using Python and R
---
This project was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and [BasalCell](https://github.com/yo-aka-gene/BasalCell) version {{cookiecutter.__version}}
