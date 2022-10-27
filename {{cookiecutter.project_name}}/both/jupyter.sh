#!/bin/sh

docker $1 {{cookiecutter.project_name}}-jupyterlab-1

if [ $1 = start ]; then
    open http://localhost:8888
fi
