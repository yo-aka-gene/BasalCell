FROM jupyter/datascience-notebook:{{cookiecutter.jupyterlab_ver}}

RUN pip install --upgrade pip
RUN pip install jupyterlab
RUN jupyter serverextension enable --py jupyterlab

WORKDIR $HOME
RUN mkdir codes data outputs utils

EXPOSE 8888

CMD ['/bin/bash']
