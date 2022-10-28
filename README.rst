=========
Basalcell
=========

Note: beta version

.. image:: https://readthedocs.org/projects/basalcell/badge/?version=latest
        :target: https://basalcell.readthedocs.io/en/latest/?version=latest

A Docker-based project scaffold generator for bioinformatics analysis


* Free software: MIT license
* Documentation: https://basalcell.readthedocs.io.

Features
--------
* cookiecutter template for distributable data analysis environment using docker
* docker container for jupyterlab or rstudio (or both) can be generated

Usage
-----
* install cookiecutter to your local environment
.. code-block:: pip install -U cookiecutter
* To create new project, run
.. code-block:: cookiecutter git@github.com:yo-aka-gene/BasalCell.git

Products
--------
* docker container
* Makefile
* shell scripts
* README.md

.. image:: ./{{cookiecutter.project_name}}logos/default.png
   :align: center
