# {{cookiecutter.project_name}}
[![DOI](https://img.shields.io/badge/DOI-wip-blue.svg?longCache=true)]()
[![PMID](https://img.shields.io/badge/PMID-wip-orange.svg?longCache=true)]()
<div align="center">
<img src="./docs/_static/default_logo.png" alt="graphical abstract" width="300" height="300" title="graphical abstract">
</div>

{%- if cookiecutter.description != "" %}
{{cookiecutter.description}}
{%- endif %}

## User Guide
### :warning: For Windows Users
- Please make sure to access this directory via `WSL`
- if `make` and `miniconda` is not available in your env, run:
```bash
sudo apt update && sudo apt install make miniconda
```

{% set use_r = cookiecutter.r_ver != 'none' -%}

### Setting the Virtual Env
1. Fork this repository and clone it to your local environment
2.  Run the initialization command:
```bash
make init
```
{% if use_r %}
(This command will automatically install Python dependencies, register the Jupyter kernel, and build the R virtual environment).
{% else %}
(This command will automatically install Python dependencies and register the Jupyter kernel).
{% endif %}

### Launching Jupyter Lab
```bash
make launch
```

### Adding Packages
This project uses a unified interface to add dependencies:
- **Python**: `make add-py PKG=name` (or `add-pydev` for dev tools)
    - overwrite `poetry.lock` with `make lock-py`
    - install dependencies listed in `poetry.lock` with `make install-py`
- **R**: `make add-r PKG=name` (or `add-bioc` for Bioconductor)
- **OS**: `make add-os PKG=name` (for conda/system libraries)

### Update Version Tags
```bash
make bump-patch  # 0.1.0 -> 0.1.1
make bump-minor  # 0.1.1 -> 0.2.0
make bump-major  # 0.2.0 -> 1.0.0
```

### Data Installation
***describe how to install your dataset(s)***

## Copyright of Data
***describe the copyright and licensing of your dataset(s)***

## Author(s)
- {{cookiecutter.author_name}} <[{{cookiecutter.email}}](mailto:{{cookiecutter.email}})>
    - GitHub account: [{{cookiecutter.github_username}}](https://github.com/{{cookiecutter.github_username}})
---
This project was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and [BasalCell](https://github.com/yo-aka-gene/BasalCell)
