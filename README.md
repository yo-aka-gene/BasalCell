# BasalCell
![version](https://img.shields.io/badge/BasalCell-v.1.0.0-blue.svg?longCache=true)
![docker](https://img.shields.io/badge/DockerCompose-3-2496ed.svg?longCache=true&logo=docker)
[![jupyter](https://img.shields.io/badge/jupyterlab-latest|lab3.4.5-f37626.svg?longCache=true&logo=jupyter)](https://hub.docker.com/r/jupyter/datascience-notebook)
[![rstudio](https://img.shields.io/badge/rstudio-latest|4-75aadb.svg?longCache=true&logo=rstudio)](https://hub.docker.com/r/rocker/tidyverse)


- Free software: MIT license

## Features
- [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for distributable data analysis environment using docker
- docker container for jupyterlab or rstudio (or both) can be generated

## Usage
- install cookiecutter to your local environment
```
pip install -U cookiecutter
```
- To create a new project, run
```
cookiecutter git@github.com:yo-aka-gene/BasalCell.git
```

## Contents (v.1.0.0)
- docker container
- Makefile
- shell scripts
- README file

### Docker container
- you can choose a configuration from below;
    - jupyterlab (datascience-notebook): version `lab-3.4.5` or `latest`
    - rstudio (rocker/tidyverse): version `4` or `latest`
    - or both
- package dependency info is exported as `requirements_py.txt` or `requirements_r.csv`
    - you can add other packages in the list afterwards.

### Makefile
- some make cmds are preset for building initial environments
- it's good to add customized make cmds to make your environment reproducible and distributable in such cases as follows;
    - downloading large data
    - installation of non-default software for linux os

### Shell scripts
- shell scripts are designed to reduce cli operations
- `auth.sh` adjusts user id for every local environment. This script is automatically executed and you don't need to mannually run codes.
- `jupyter.sh` can start/stop docker containers of jupyterlab by `sh jupyter.sh start` or `sh.jupyter.sh stop`
- `rstudio.sh` can start/stop docker containers of rstudio by `sh rstudio.sh start` or `sh.rstudio.sh stop`

### README file
- appropriate README file (for your configuration of docker containers) will be generated
- defaul README file includes a default image as follows;
<div align="center">
<img src="./{{cookiecutter.project_name}}/logos/default.png" alt="graphical abstract" width="300" height="300" title="graphical abstract">
</div>

- you can replace the image as you like (e.g., graphical abstract for your research article)

## Future work (v.1.0.0)
- Unit test option (`pytest` etc.)
- lint option (`flake8`, `black` etc.)
- documentation option (`sphinx` etc.)
