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
- if `make` is not available in your env, run:
```bash
sudo apt update && sudo apt install make
```

{% set use_r = cookiecutter.r_ver != 'none' -%}

### Setting the Virtual Env
1. Fork this repository and clone it to your local environment
2. Ensure you have Python `>="{{ cookiecutter.python_ver }}",<4.0` (e.g., via `pyenv`) installed.
3. Install `poetry` (using `pipx` is highly recommended to avoid environment conflicts):
```bash
pipx install poetry
```
4.  Run the initialization command:
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

### Data Installation
***describe how to install your dataset(s)***

## Copyright of Data
***describe the copyright and licensing of your dataset(s)***

## Author(s)
- {{cookiecutter.author_name}} <[{{cookiecutter.email}}](mailto:{{cookiecutter.email}})>
    - GitHub account: [{{cookiecutter.github_username}}](https://github.com/{{cookiecutter.github_username}})
---
This project was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and [BasalCell](https://github.com/yo-aka-gene/BasalCell)
