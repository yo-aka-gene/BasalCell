#!/bin/sh

sh auth.sh docker-compose.yml
docker compose up -d

{% set use_jupyter = cookiecutter.jupyterlab_ver != 'none' -%}
{% set unit_test = cookiecutter.unit_test != 'no' -%}
{% set lint = cookiecutter.lint != 'no' -%}

{% if use_jupyter and unit_test %}
docker exec {{cookiecutter.project_name}}-jupyterlab-1 pip install pytest
{% endif %}

{% if use_jupyter and lint %}
docker exec {{cookiecutter.project_name}}-jupyterlab-1 pip install flake8
{% endif %}

make write-lib

if [[ -e jupyter.sh ]]; then
    sh jupyter.sh stop
fi

if [[ -e rstudio.sh ]]; then
    sh rstudio.sh stop
fi

nb_id=$(id -u)
sed -i '' -e s/${nb_id}/YOUR_ID/ docker-compose.yml
