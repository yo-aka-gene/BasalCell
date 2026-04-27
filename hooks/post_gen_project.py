import os
import shutil
import subprocess
import sys


def is_tool_installed(name):
    return shutil.which(name) is not None


def setup_symbolic_links():
    print("Setting up symbolic links for Jupyter Notebooks...")
    links = [
        {
            "src": "../../{{cookiecutter.__project_slug}}_rtools",
            "dest": "docs/jupyternb/{{cookiecutter.__project_slug}}_rtools",
        },
        {
            "src": "../../{{cookiecutter.__project_slug}}_tools",
            "dest": "docs/jupyternb/{{cookiecutter.__project_slug}}_tools",
        },
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


if __name__ == "__main__":
    print("Cookiecutter project generation: Done!")
    setup_symbolic_links()
    use_r = "{{ cookiecutter.r_ver }}".lower() != "none"
    if not use_r:
        r_files = ["setup_r_env.sh", ".lintr"]
        for f in r_files:
            if os.path.exists(f):
                os.remove(f)
        shutil.rmtree("{{cookiecutter.__project_slug}}_rtools")

    create_package = "{{ cookiecutter.create_package }}".lower() == "true"
    if not create_package and os.path.exists("src"):
        shutil.rmtree("src")

    has_conda = is_tool_installed("conda")
    has_make = is_tool_installed("make")

    if has_conda and has_make:
        try:
            print("Running 'make init'... This may take a few minutes.")
            subprocess.run(["make", "init"], check=True)
            print(
                "Run 'conda activate conda_{{cookiecutter.__project_slug}}'"
                "to access to conda_{{cookiecutter.__project_slug}} env from terminal."
            )
        except subprocess.CalledProcessError:
            print("\n[ERROR] 'make init' failed.")
            print(
                "Please check your internet connection or "
                "conda configuration and run 'make init' manually."
            )
            sys.exit(1)
    else:
        print("\n[NOTICE] Automatic environment setup was skipped.")
        if not has_conda:
            print(
                "  - 'conda' command not found. Please install Miniconda or Anaconda."
            )
        if not has_make:
            print(
                "  - 'make' command not found. "
                "Please install 'make' (e.g., sudo apt install make)."
            )
        print(
            "\nAfter installing missing tools, "
            "run 'make init' in the project directory."
        )
