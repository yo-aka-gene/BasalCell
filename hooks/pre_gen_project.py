import sys

ignore_jup = "{{cookiecutter.jupyterlab_ver}}" == "none"
ignore_r = "{{cookiecutter.jupyterlab_ver}}" == "none"

if ignore_jup and ignore_r:
    print("ERROR: Specify versions of Docker images at least either of jupyterlab or rstudio")
    sys.exit(1)
