#!/bin/sh

sh auth.sh docker-compose.yml
docker compose up -d

sh linux_deps.sh

{% if cookiecutter.unit_test == "yes" %}
docker exec {{cookiecutter.project_name}}-jupyterlab-1 pip install pytest
{% endif %}

{% if cookiecutter.lint == "yes" %}
docker exec {{cookiecutter.project_name}}-jupyterlab-1 pip install flake8
{% endif %}

make write-lib
sh jupyter.sh stop
sh rstudio.sh stop

nb_id=$(id -u)
sed -i '' -e s/${nb_id}/YOUR_ID/ docker-compose.yml
