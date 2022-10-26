import os
import shutil
import sys

use_jup = {{cookiecutter.jupyterlab_ver}} != "none"
use_r = {{cookiecutter.jupyterlab_ver}} != "none"

if use_jup and use_r:
    os.remove("Makefile_py")
    os.remove("Makefile_r")
    shutil.move("Makefile_both", "Makefile")

elif use_jup:
    os.remove("Makefile_both")
    os.remove("Makefile_r")
    os.remove("utils/export_deps.R")
    os.remove("utils/install_deps.R")
    os.remove("utils/requirements_r.csv")
    shutil.move("Makefile_py", "Makefile")

else:
    os.remove("Makefile_both")
    os.remove("Makefile_py")
    os.remove("utils/__init__.py")
    os.remove("utils/requirements_py.txt")
    shutil.move("Makefile_r", "Makefile")

