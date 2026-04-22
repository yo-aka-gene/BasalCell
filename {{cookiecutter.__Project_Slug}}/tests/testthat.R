library(testthat)

{%- if cookiecutter.create_package == "true" %}
test_check("{{ cookiecutter.__project_slug }}")
{%- else %}
test_dir("tests/testthat")
{%- endif %}
