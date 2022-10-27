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
    path = "both"

elif use_jup:
    shutil.rmtree("both")
    shutil.rmtree("rs")
    path = "jup"

else:
    shutil.rmtree("both")
    shutil.rmtree("jup")
    path = "rs"

for file in glob.glob(f"{path}/*"):
    shutil.move(file, ".")
    
os.rmdir(path)
subprocess.run(["sh", "init.sh"])

for file in glob.glob(f"build_{path}/*"):
    shutil.move(file, ".")

for build_dir in glob.glob("build_*"):
    shutil.rmtree(build_dir)
