#!/bin/sh

{% set use_rstudio = cookiecutter.rstudio_ver != 'none' -%}
{% if use_rstudio %}
docker $1 {{cookiecutter.project_name}}-rstudio-1

if [ $1 = start ]; then
    open http://localhost:8787
fi
{% else %}
rm -f rstudio.sh
{% endif %}
