{% set use_jupyter = cookiecutter.jupyterlab_ver != 'none' -%}
{% set use_rstudio = cookiecutter.rstudio_ver != 'none' -%}
{% if use_jupyter and use_rstudio %}
.PHONY: clean clean-build clean-pyc init lib lib-py lib-r write-lib terminate reboot help
{% else %}
.PHONY: clean clean-build clean-pyc init lib write-lib terminate reboot help
{% endif %}
.DEFAULT_GOAL := help

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

init: ## setup essentials
	sh auth.sh docker-compose.yml
	docker compose up -d
{% if use_jupyter and use_rstudio %}
	sh linux_deps.sh
{% endif %}
	make lib
{% if use_jupyter %}
	sh jupyter.sh start
{% endif %}
{% if use_rstudio %}
	sh rstudio.sh start
{% endif %}

{% if use_jupyter and use_rstudio %}
lib: lib-py lib-r

lib-py: ## install required packages in Python
	docker exec {{cookiecutter.project_name}}-jupyterlab-1 python -m pip install -r ./utils/requirements_py.txt

lib-r: ## install required packages in R
	docker exec {{cookiecutter.project_name}}-rstudio-1 Rscript ./home/rstudio/utils/install_deps.R

write-lib: ## export reqired packages
	docker exec {{cookiecutter.project_name}}-jupyterlab-1 pip list --format=freeze > ./utils/requirements_py.txt
	docker exec {{cookiecutter.project_name}}-rstudio-1 Rscript ./home/rstudio/utils/export_deps.R
{% elif use_jupyter %}
lib: ## install required packages in Python
	docker exec {{cookiecutter.project_name}}-jupyterlab-1 python -m pip install -r ./utils/requirements_py.txt

write-lib: ## export reqired packages
	docker exec {{cookiecutter.project_name}}-jupyterlab-1 pip list --format=freeze > ./utils/requirements_py.txt
{% elif use_rstudio %}
lib: ## install required packages in R
	docker exec {{cookiecutter.project_name}}-rstudio-1 Rscript ./home/rstudio/utils/install_deps.R

write-lib: ## export reqired packages
	docker exec {{cookiecutter.project_name}}-rstudio-1 Rscript ./home/rstudio/utils/export_deps.R
{% endif %}

terminate: ## remove docker container
	docker compose down

reboot: ## remove and rebuild docker container
	make terminate
	make init

help: ## user guide
	open Makefile
