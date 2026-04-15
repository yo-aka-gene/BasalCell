# tests/testthat.R
library(testthat)

{%- if cookiecutter.create_packate == "true" %}
test_check("{{ cookiecutter.__project_slug }}")
{%- else %}
test_dir("tests/testthat")
{%- endif %}
