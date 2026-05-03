# Welcome to {{cookiecutter.project_name}}'s documentation!

{%- if cookiecutter.create_package == "true" %}
## Add API reference headder as follows:
<!-- ```{toctree}
:maxdepth: 2
:caption: API Refernce

notebooks
``` -->
{%- endif %}
## Add your Analysis Code Gallery headder as follows:
```{toctree}
:maxdepth: 2
:caption: Analysis Code Gallery

notebooks
```
## Add API reference headder for your auxiliary created in `{{cookiecutter.__project_slug}}_tools` as follows:
<!-- ```{toctree}
:maxdepth: 2
:caption: Auxiliary Python Scripts 

tools
``` -->
{% if cookiecutter.r_ver != "none" %}
## R Resources (pkgdown)
For detailed documentation of the R tools and utilities used in this project, please refer to the following pages:
<ul>
  <li><a href="r_api/index.html">R API Reference</a></li>
  <li><a href="r_api/reference/index.html">Function Reference</a></li>
  <li><a href="r_api/articles/index.html">Vignettes Reference</a></li>
</ul>
{% endif %}

## About
- Author: {{ cookiecutter.author_name }}
- Contact: [{{ cookiecutter.email }}](mailto:{{ cookiecutter.email }})
- GitHub: [@{{ cookiecutter.github_username }}](https://github.com/{{ cookiecutter.github_username }})
---
This project was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and [BasalCell](https://github.com/yo-aka-gene/BasalCell) version {{cookiecutter.__version}}
