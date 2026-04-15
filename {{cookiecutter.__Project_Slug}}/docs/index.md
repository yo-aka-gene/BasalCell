```{include} ../README.md
```

## Table of Contents

```{toctree}
:maxdepth: 2
:caption: Analysis Notebooks

# add `.ipynb` files for analyses
# （omit `.ipynb` file extensions）
# 
# examples:
# jupyternb/01_data_preprocessing
# jupyternb/02_clustering
# jupyternb/03_differential_expression
```
{% if cookiecutter.create_package == "true" %}
```{toctree}
:maxdepth: 2
:caption: API Reference

# add documents for each module here
# examples:
# {{ cookiecutter.__project_slug }}/modules
```
{% endif %}

## About
- Author: {{ cookiecutter.author_name }}
- Contact: [{{ cookiecutter.email }}](mailto:{{ cookiecutter.email }})
- GitHub: [@{{ cookiecutter.github_username }}](https://github.com/{{ cookiecutter.github_username }})
---
This project was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and [BasalCell](https://github.com/yo-aka-gene/BasalCell)
