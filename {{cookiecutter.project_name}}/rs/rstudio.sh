#!/bin/sh

docker $1 {{cookiecutter.project_name}}-rstudio-1

if [ $1 = start ]; then
    open http://localhost:8787
fi
