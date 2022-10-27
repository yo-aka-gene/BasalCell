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
    shutil.rmtree("utils/jup")
    shutil.rmtree("utils/rs")
    path = "both"

elif use_jup:
    shutil.rmtree("both")
    shutil.rmtree("rs")
    shutil.rmtree("utils/both")
    shutil.rmtree("utils/rs")
    path = "jup"

else:
    shutil.rmtree("both")
    shutil.rmtree("jup")
    shutil.rmtree("utils/both")
    shutil.rmtree("utils/jup")
    path = "rs"

for file in glob.glob(f"{path}/*"):
    shutil.move(file, ".")

for file in glob.glob(f"utils/{path}/*"):
    shutil.move(file, "utils")
    
os.rmdir(path)
os.rmdir(f"utils/{path}")
subprocess.run(["sh", "init.sh"])

for file in ["docker-compose.yml", "auth.sh", "init.sh"]:
    os.remove(file)

for file in glob.glob(f"build_{path}/*"):
    shutil.move(file, ".")

for build_dir in glob.glob("build_*"):
    shutil.rmtree(build_dir)
