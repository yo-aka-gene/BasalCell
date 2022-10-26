import os
import shutil
import sys

use_jup = "{{cookiecutter.jupyterlab_ver}}" != "none"
use_r = "{{cookiecutter.rstudio_ver}}" != "none"

if use_jup and use_r:
    os.remove("Makefile_py")
    os.remove("Makefile_r")
    os.remove("Dockerfile_py")
    os.remove("Dockerfile_r")
    os.remove("py_docker-compose.yml")
    os.remove("r_docker-compose.yml")
    shutil.move("Makefile_both", "Makefile")
    shutil.move("Dockerfile_both", "Dockerfile")
    shutil.move("both_docker-compose.yml", "docker-compose.yml")

elif use_jup:
    os.remove("Makefile_both")
    os.remove("Makefile_r")
    os.remove("Dockerfile_both")
    os.remove("Dockerfile_r")
    os.remove("both_docker-compose.yml")
    os.remove("r_docker-compose.yml")
    os.remove("utils/export_deps.R")
    os.remove("utils/install_deps.R")
    os.remove("utils/requirements_r.csv")
    shutil.move("Makefile_py", "Makefile")
    shutil.move("Dockerfile_py", "Dockerfile")
    shutil.move("py_docker-compose.yml", "docker-compose.yml")

else:
    os.remove("Makefile_both")
    os.remove("Makefile_py")
    os.remove("Dockerfile_both")
    os.remove("Dockerfile_py")
    os.remove("both_docker-compose.yml")
    os.remove("py_docker-compose.yml")
    os.remove("utils/__init__.py")
    os.remove("utils/requirements_py.txt")
    os.remove("utils/auth.sh")
    shutil.move("Makefile_r", "Makefile")
    shutil.move("Dockerfile_r", "Dockerfile")
    shutil.move("r_docker-compose.yml", "docker-compose.yml")

