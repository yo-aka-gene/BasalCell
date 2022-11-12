# {{cookiecutter.project_name}}
[![DOI](https://img.shields.io/badge/DOI-wip-blue.svg?longCache=true)]()
[![PMID](https://img.shields.io/badge/PMID-wip-orange.svg?longCache=true)]()
<div align="center">
<img src="./logos/default.png" alt="graphical abstract" width="300" height="300" title="graphical abstract">
</div>

{% if cookiecutter.description != "" %}
{{cookiecutter.description}}
{% endif %}

## User Guide
### For Windows Users
- Please make sure that you can run shell scripts and `make` cmds in your local environment.
    - you can install it using [Chocolately](https://chocolatey.org/): `choco install make`

{% set use_jupyter = cookiecutter.jupyterlab_ver != 'none' -%}
{% set use_rstudio = cookiecutter.rstudio_ver != 'none' -%}
### Setting the Virtual Env
1. fork this repository and clone it to your local environment
2. install Docker into your local environment (if already satisfied, skip this)
3. run `make init` cmd in the cloned directory. (**WARNING**: if you rather not use the make cmd, you need to run `auth.sh` to specify your user id)
{% if use_jupyter and use_rstudio %}
4. jupyterlab and rtudio is succesfully launched (password for jupyterlab: `jupyter`). **Note**: some linux packages are pre-installed. See also `linux_deps.sh`.
    - jupyterlab: `localhost:8888`
    - rstudio: `localhost:8777`
{% elif use_jupyter %}
4. jupyterlab is succesfully launched (password: `jupyter`).
    - jupyterlab: `localhost:8888`
{% elif use_rstudio %}
4. rtudio is succesfully launched. **Note**: some linux packages are pre-installed. See also `Dockerfile`.
    - rstudio: `localhost:8777`
{% endif %}
### Starting or Stopping the Virtual Env
{% if use_jupyter and use_rstudio -%}
#### Jupyterlab
- to start jupyterlab, run;
```
sh jupyter.sh start
```
- to stop jupyterlab, run;
```
sh jupyter.sh stop
```
#### Rstudio
- to start rstudio, run;
```
sh rstudio.sh start
```
- to stop rstudio, run;
```
sh rstudio.sh stop
```
{% elif use_jupyter %}
- to start jupyterlab, run;
```
sh jupyter.sh start
```
- to stop jupyterlab, run;
```
sh jupyter.sh stop
```
{% elif use_rstudio %}
- to start rstudio, run;
```
sh rstudio.sh start
```
- to stop rstudio, run;
```
sh rstudio.sh stop
```
{% endif %}

### Data Installation

## Copyright of Data

## Author(s)
- {{cookiecutter.author_name}} <[{{cookiecutter.email}}](mailto:{{cookiecutter.email}})>
    - GitHub account: [{{cookiecutter.github_username}}](https://github.com/{{cookiecutter.github_username}})
---
This project was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and [BasalCell](https://github.com/yo-aka-gene/BasalCell)
