import glob
import os
import shutil
import subprocess

use_jup = "{{cookiecutter.jupyterlab_ver}}" != "none"
use_r = "{{cookiecutter.rstudio_ver}}" != "none"
unit_test = "{{cookiecutter.unit_test}}" != "no"
prj_name = "{{cookiecutter.project_name}}"

if use_jup and use_r:
    shutil.rmtree("jup")
    shutil.rmtree("rs")
    shutil.rmtree("utils/jup")
    shutil.rmtree("utils/rs")
    shutil.rmtree("tests/jup")
    shutil.rmtree("tests/rs")
    path = "both"

elif use_jup:
    shutil.rmtree("both")
    shutil.rmtree("rs")
    shutil.rmtree("utils/both")
    shutil.rmtree("utils/rs")
    shutil.rmtree("tests/both")
    shutil.rmtree("tests/rs")
    path = "jup"

else:
    shutil.rmtree("both")
    shutil.rmtree("jup")
    shutil.rmtree("utils/both")
    shutil.rmtree("utils/jup")
    shutil.rmtree("tests/both")
    shutil.rmtree("tests/jup")
    path = "rs"

for file in glob.glob(f"{path}/*"):
    shutil.move(file, "./init.sh" if "init" in file else ".")

for file in glob.glob(f"utils/{path}/*"):
    shutil.move(file, "utils")

for file in glob.glob(f"tests/{path}/*"):
    shutil.move(file, "tests")
    
os.rmdir(path)
os.rmdir(f"utils/{path}")
os.rmdir(f"tests/{path}")

if not unit_test:
    shutil.rmtree("tests")

subprocess.run(["sh", "init.sh"])

for file in ["auth.sh", "init.sh"]:
    os.remove(file)

os.remove("_auth.sh") if path == "rs" else shutil.move("_auth.sh", "auth.sh")

print(f"{prj_name} is successfully generated: push to your github repository before you edit it")
