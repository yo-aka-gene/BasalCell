{% set only_rstudio = cookiecutter.jupyterlab_ver == 'none' -%}
{% if only_rstudio %}
FROM rocker/tidyverse:{{cookiecutter.rstudio_ver}}

RUN apt-get update
RUN apt-get install -y \
libcurl4-openssl-dev \
libssl-dev libjq-dev \
libprotobuf-dev \
protobuf-compiler \
make \
libgeos-dev \
libglpk40 \
libudunits2-dev \
libgdal-dev \
gdal-bin \
libproj-dev \
libv8-dev

CMD ['/bin/bash']
{% else %}
FROM jupyter/datascience-notebook:{{cookiecutter.jupyterlab_ver}}

RUN pip install --upgrade pip
RUN pip install jupyterlab
RUN jupyter serverextension enable --py jupyterlab

WORKDIR $HOME
RUN mkdir codes data outputs utils
RUN rmdir work

EXPOSE 8888

CMD ['/bin/bash']
{% endif %}
