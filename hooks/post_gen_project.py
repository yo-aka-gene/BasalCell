import glob
import os
import shutil
import subprocess
import sys

use_jup = "{{cookiecutter.jupyterlab_ver}}" != "none"
use_r = "{{cookiecutter.rstudio_ver}}" != "none"

if use_jup and use_r:
    shutil.rmtree("jup")
    shutil.rmtree("rs")
    for file in glob.glob("both/*"):
        shutil.move(file, ".")
    os.rmdir("both")

elif use_jup:
    shutil.rmtree("both")
    shutil.rmtree("rs")
    for file in glob.glob("jup/*"):
        shutil.move(file, ".")
    os.rmdir("jup")

else:
    shutil.rmtree("both")
    shutil.rmtree("jup")
    for file in glob.glob("rs/*"):
        shutil.move(file, ".")
    os.rmdir("rs")
