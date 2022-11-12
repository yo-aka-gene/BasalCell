#!/bin/sh

sh auth.sh docker-compose.yml
docker compose up -d

{% set use_jupyter = cookiecutter.jupyterlab_ver != 'none' -%}

sh linux_deps.sh

make write-lib
sh jupyter.sh stop
sh rstudio.sh stop

{% if use_jupyter %}
nb_id=$(id -u)
sed -i '' -e s/${nb_id}/YOUR_ID/ docker-compose.yml
{% endif %}
