# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import glob
import os
import sys

# -- Path setup and Versioning -----------------------------------------------
{%- if cookiecutter.create_package == "true" %}
sys.path.insert(0, os.path.abspath("../src"))

import {{ cookiecutter.__project_slug }}
release = {{ cookiecutter.__project_slug }}.__version__
{%- else %}
# If not a package, default version is used.
release = "0.0.1"
{%- endif %}

# -- Project information -----------------------------------------------------
project = "{{ cookiecutter.project_name }}"
author = "{{ cookiecutter.author_name }}"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",     # NumPy/Google style docstrings
    "sphinx.ext.viewcode",
    "nbsphinx",                # Jupyter Notebook support
    "sphinx_gallery.load_style",
    "myst_parser",             # Markdown support
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "_static/default_logo.png"

html_theme_options = {
    "navigation_depth": 5,
    "logo_only": True,
}

htmlhelp_basename = "{{ cookiecutter.__project_slug }}"

# -- Options for LaTeX output ------------------------------------------------
latex_documents = [
    ("index", "{{ cookiecutter.__project_slug }}.tex",
     "{{ cookiecutter.project_name }} Analysis Details",
     author, "manual"),
]

# -- Options for manual page output ------------------------------------------
man_pages = [
    ("index", "{{ cookiecutter.__project_slug }}",
     "{{ cookiecutter.project_name }} Analysis Details",
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    ("index", "{{ cookiecutter.__project_slug }}",
     "{{ cookiecutter.project_name }} Analysis Details",
     author,
     "{{ cookiecutter.__project_slug }}",
     "{{ cookiecutter.description }}",
     "Miscellaneous"),
]

sys.path.insert(0, os.path.abspath('./jupyternb'))

# -- Setting Thumbnails for nbsphinx -----------------------------------------
nbsphinx_thumbnails = {
    "/".join(
        v.split(".")[:-1]
    ): v.replace(
        "jupyternb", "_static"
    ).replace(
        "ipynb", "png"
    ) if os.path.exists(
        v.replace(
            "jupyternb", "_static"
        ).replace(
            "ipynb", "png"
        )
    ) else "_static/default_logo.png" for v in glob.glob("jupyternb/*")
}
