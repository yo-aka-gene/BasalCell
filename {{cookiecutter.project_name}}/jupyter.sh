#!/bin/sh

{% set use_jupyter = cookiecutter.jupyterlab_ver != 'none' -%}
{% if use_jupyter %}
docker $1 {{cookiecutter.project_name}}-jupyterlab-1

if [ $1 = start ]; then
    open http://localhost:8888
fi
{% else %}
rm -f jupyter.sh
{% endif %}
