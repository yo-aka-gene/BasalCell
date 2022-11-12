#!/bin/sh

{% set use_jupyter = cookiecutter.jupyterlab_ver != 'none' -%}
{% set use_rstudio = cookiecutter.rstudio_ver != 'none' -%}
{% if use_jupyter and use_rstudio %}
docker exec {{cookiecutter.project_name}}-rstudio-1 apt-get update
docker exec {{cookiecutter.project_name}}-rstudio-1 apt-get install -y \
libcurl4-openssl-dev libssl-dev libjq-dev libprotobuf-dev protobuf-compiler \
make libgeos-dev libglpk40 libudunits2-dev libgdal-dev gdal-bin libproj-dev libv8-dev
{% else %}
rm -f linux_deps.sh
{% endif %}
