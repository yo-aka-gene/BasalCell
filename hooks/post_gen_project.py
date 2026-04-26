import os
import shutil
import site
import subprocess
import sys


def is_tool_installed(name):
    return shutil.which(name) is not None


def install_poetry():
    print("Installing Poetry")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "poetry"], check=True)
        print("Installing Poetry: Done!")

        if os.name == "nt":
            user_bin = os.path.join(site.USER_BASE, "Scripts")
        else:
            user_bin = os.path.join(site.USER_BASE, "bin")

        py_bin = os.path.dirname(sys.executable)
        os.environ["PATH"] = (
            f"{user_bin}{os.pathsep}{py_bin}{os.pathsep}{os.environ.get('PATH', '')}"
        )

        poetry_path = shutil.which("poetry")
        if poetry_path:
            installed_dir = os.path.dirname(poetry_path)
            print(f"Note: Poetry was installed to {installed_dir}")
        else:
            print(
                "Note: Poetry was installed, but its location could not be determined."
            )
        print("If 'poetry' command is not found, please restart your terminal.")

    except subprocess.CalledProcessError:
        print("Failed in Poetry Installation")
        sys.exit(1)


def setup_symbolic_links():
    print("Setting up symbolic links for Jupyter Notebooks...")
    links = [
        {"src": "../R", "dest": "tools/R"},
        {"src": "../../tools", "dest": "docs/jupyternb/tools"},
        {"src": "../../data", "dest": "docs/jupyternb/data"},
    ]

    for link in links:
        src = link["src"]
        dest = link["dest"]

        dest_dir = os.path.dirname(dest)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)

        if os.path.lexists(dest):
            if os.path.isdir(dest) and not os.path.islink(dest):
                shutil.rmtree(dest)
            else:
                os.remove(dest)

        try:
            os.symlink(src, dest)
            print(f"  - Created link: {dest} -> {src}")
        except Exception as e:
            print(f"  - [WARNING] Failed to create link {dest}: {e}")
            print("If you are on Windows, ensure Developer Mode is ON or run as Admin.")


if __name__ == "__main__":
    print("Cookiecutter project generation: Done!")
    setup_symbolic_links()
    use_r = "{{ cookiecutter.r_ver }}".lower() != "none"
    if not use_r and os.path.exists("setup_r_env.sh"):
        os.remove("setup_r_env.sh")
        os.remove(".lintr")
        os.remove("tests/testthat.R")
        shutil.rmtree("tests/testthat")

    create_package = "{{ cookiecutter.create_package }}".lower() == "true"
    if not create_package and os.path.exists("src"):
        shutil.rmtree("src")

    if not is_tool_installed("poetry"):
        install_poetry()

    if is_tool_installed("make"):
        try:
            subprocess.run(["make", "init"], check=True)
            print("Env setup: Done!")
        except subprocess.CalledProcessError:
            print("Failed in 'make init' execution")
            sys.exit(1)

    else:
        print("'make' command is not found; halting env setup")
        print("[for Windows users] run the code below via WSL")
        print("sudo apt update && sudo apt install make")
        print("then run `make init` in this directory")
        sys.exit(1)
