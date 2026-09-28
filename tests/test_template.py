"""
Test for BasalCell template generation
"""

import json
import subprocess
import tomllib

import pytest
import yaml


@pytest.fixture
def prj_slug():
    return "REPLACETHIS"


@pytest.fixture
def essential_chs():
    return ["conda-forge", "bioconda", "nodefaults"]


@pytest.fixture
def essential_deps():
    return [
        "python",
        "poetry",
        "poetry-plugin-export",
        "make",
        "git",
        "yq",
        "jq",
        "cmake",
        "c-compiler",
        "cxx-compiler",
        "pre-commit",
    ]


@pytest.fixture
def essential_files():
    return [
        ".gitignore",
        ".pre-commit-config.yaml",
        ".readthedocs.yaml",
        "environment.yml",
        "Makefile",
        "poetry.lock",
        "poetry.toml",
        "pyproject.toml",
        "README.md",
        ".basalcell/basalcell_system/__init__.py",
        ".basalcell/conda-lock.yml",
        ".github/workflows/test.yml",
        ".github/pull_request_template.md",
        "REPLACETHIS_tools/__init__.py",
        "data/.gitkeep",
        "docs/_static/default_logo.png",
        "docs/jupyternb/output/.gitkeep",
        "docs/conf.py",
        "docs/index.md",
        "tests/__init__.py",
    ]


@pytest.fixture
def symbolic_links():
    return [
        "docs/jupyternb/data",
        "docs/jupyternb/REPLACETHIS_tools",
    ]


@pytest.fixture
def rlang_deps():
    return [
        "fortran-compiler",
        "r-base",
        "r-renv",
        "r-irkernel",
        "r-testthat",
        "r-styler",
        "r-lintr",
        "r-devtools",
        "r-pkgdown",
        "r-roxygen2",
        "r-rmarkdown",
        "r-knitr",
        "r-biocmanager",
        "bioconductor-biocversion",
    ]


@pytest.fixture
def rlang_files():
    return [
        ".lintr",
        "renv.lock",
        ".Renviron",
        ".Rprofile",
        "REPLACETHIS_rtools/DESCRIPTION",
        "REPLACETHIS_rtools/_pkgdown.yml",
        "REPLACETHIS_rtools/R/.gitkeep",
        "REPLACETHIS_rtools/tests/testthat.R",
        "REPLACETHIS_rtools/tests/testthat/.gitkeep",
        "REPLACETHIS_rtools/vignettes/example.Rmd",
        "renv/activate.R",
        "renv/settings.json",
    ]


@pytest.fixture
def rlang_symbolic_links():
    return [
        "docs/jupyternb/data",
        "docs/jupyternb/REPLACETHIS_tools",
        "docs/jupyternb/REPLACETHIS_rtools",
    ]


def get_project_jupyter(project_path):
    jupyter = project_path / ".venv" / "bin" / "jupyter"
    assert jupyter.exists(), f"Jupyter executable not found: {jupyter}"
    return str(jupyter)


def uninstall_kernel(name, cwd):
    uninstall_cmd = [get_project_jupyter(cwd), "kernelspec", "uninstall", "-y", name]
    subprocess.run(uninstall_cmd, cwd=cwd, capture_output=True, text=True)


def check_bake_result(result, idx):
    print("===== #1. Checking exit code =====")
    if result.exit_code != 0:
        raise result.exception
    # assert (
    #     result.exit_code == 0
    # ), f"FAILED in #1! Invalid exit_code; expected 0, got {result.exit_code}"

    print("===== #2. Checking exception status =====")
    assert (
        result.exception is None
    ), f"FAILED in #2! Invalid exception; expected None, got {result.exception}"

    print("===== #3. Checking project directory path =====")
    path = result.project_path.name
    assert (
        path == f"Test_Project_CI_CD_{idx}"
    ), f"FAILED in #3-1! Invalid path; expected `Test_Project_CI_CD_{idx}`, got {path}"

    assert result.project_path.is_dir(), f"FAILED in #3-2! {path} is not a directory"


def minimal_project_tests(
    project_path,
    project_name,
    fixture_essential_chs,
    fixture_essential_deps,
    fixture_essential_files,
    fixture_symbolic_links,
    slug,
):
    print("===== #4. Checking Mamba environment =====")
    expected_env_name = f"mamba_{project_name.lower()}"
    mamba_proc = subprocess.run(
        ["mamba", "env", "list", "--json"], capture_output=True, text=True, check=True
    )
    env_paths = json.loads(mamba_proc.stdout).get("envs", [])
    env_exists = any(
        path.endswith(f"/{expected_env_name}")
        or path.endswith(f"\\{expected_env_name}")
        for path in env_paths
    )
    assert (
        env_exists
    ), f"FAILED in #4-1! {expected_env_name} is not found in {env_paths}"

    env_file = project_path / "environment.yml"
    with open(env_file, "r") as f:
        env_data = yaml.safe_load(f)
    channels = env_data.get("channels", [])
    dependencies = env_data.get("dependencies", [])

    for i, ch in enumerate(fixture_essential_chs):
        assert any(
            isinstance(dep, str) and dep.startswith(f"{ch}") for dep in channels
        ), f"FAILED in #4-{i + 2}! {ch} not found in channels: {channels}"

    for i, pkg in enumerate(fixture_essential_deps):
        assert any(
            isinstance(dep, str) and dep.startswith(f"{pkg}") for dep in dependencies
        ), f"FAILED in #12-{i + 2 + len(fixture_essential_chs)}! {pkg} not found"
        " in dependencies: {dependencies}"

    print("===== #5. Checking essential files =====")
    for i, file in enumerate(fixture_essential_files):
        file = (file).replace(slug, project_name.lower())
        file_path = project_path / file
        assert (
            file_path.exists()
        ), f"FAILED in #5-{i + 1}! {file} is not found in {project_name}"

    poetry_config_file = project_path / "poetry.toml"
    with open(poetry_config_file, "rb") as f:
        poetry_config = tomllib.load(f)

    assert (
        poetry_config.get("virtualenvs", {}).get("create") is True
    ), "FAILED in #5! poetry.toml must set virtualenvs.create = true"

    assert (
        poetry_config.get("virtualenvs", {}).get("in-project") is True
    ), "FAILED in #5! poetry.toml must set virtualenvs.in-project = true"

    venv_path = project_path / ".venv"
    assert venv_path.is_dir(), "FAILED in #5! project-local .venv was not created"

    print("===== #6–8. Checking symbolic links =====")
    for i, link in enumerate(fixture_symbolic_links):
        link = (link).replace(slug, project_name.lower())
        link_path = project_path / link
        expected_target_name = link.split("/")[-1]
        resolved_path = link_path.resolve()
        # #6. If it's a symbolic link?
        assert (
            link_path.is_symlink()
        ), f"FAILED in #6-{i + 1}! {link} is not a symbolic link"
        # #7. if it's not broken
        assert (
            link_path.exists()
        ), f"FAILED in #7-{i + 1}! Symbolic link {link} target is not found"
        # #8. If it's referring to the correct path
        assert (
            resolved_path.name == expected_target_name
        ), f"FAILED in #8-{i + 1}! {link} points to wrong target: {resolved_path.name}"

    print("===== #9. Checking Jupyter Kernel =====")
    kernel_name = f"{project_name.lower()}_py"
    try:
        check_cmd = [get_project_jupyter(project_path), "kernelspec", "list"]
        res = subprocess.run(
            check_cmd, cwd=project_path, capture_output=True, text=True
        )
        assert (
            res.returncode == 0
        ), f"FAILED in #9! Failed to list Jupyter kernels:\n{res.stderr}"
        assert (
            kernel_name in res.stdout.lower()
        ), f"FAILED in #9! '{kernel_name}' not found in:\n{res.stdout}"
    finally:
        uninstall_kernel(kernel_name, project_path)


def minimal_tests(
    result,
    fixture_essential_chs,
    fixture_essential_deps,
    fixture_essential_files,
    fixture_symbolic_links,
    slug,
):
    minimal_project_tests(
        result.project_path,
        result.project_path.name,
        fixture_essential_chs,
        fixture_essential_deps,
        fixture_essential_files,
        fixture_symbolic_links,
        slug,
    )


def test_correct_template(
    cookies, essential_chs, essential_deps, essential_files, symbolic_links, prj_slug
):
    result = cookies.bake(extra_context={"project_name": "Test Project-CI/CD-1"})
    check_bake_result(result, 1)
    env_name = f"mamba_{result.project_path.name.lower()}"
    try:
        minimal_tests(
            result,
            essential_chs,
            essential_deps,
            essential_files,
            symbolic_links,
            prj_slug,
        )
    finally:
        subprocess.run(
            ["mamba", "env", "remove", "-n", env_name, "-y"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def test_correct_template_for_package_mode(
    cookies, essential_chs, essential_deps, essential_files, symbolic_links, prj_slug
):
    result = cookies.bake(
        extra_context={
            "project_name": "Test Project-CI/CD-2",
            "author_name": "John Smith",
            "email": "example@example.com",
            "create_package": "true",
        }
    )
    check_bake_result(result, 2)
    env_name = f"mamba_{result.project_path.name.lower()}"
    try:
        minimal_tests(
            result,
            essential_chs,
            essential_deps,
            essential_files,
            symbolic_links,
            prj_slug,
        )

        print("===== #10. Checking Package files =====")
        path = result.project_path.name
        project_slug = path.lower()
        file = f"src/{project_slug}/__init__.py"
        file_path = result.project_path / file
        assert file_path.exists(), f"FAILED in #10! {file} is not found in {path}"

    finally:
        subprocess.run(
            ["mamba", "env", "remove", "-n", env_name, "-y"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def test_correct_template_with_rlang(
    cookies,
    essential_chs,
    essential_deps,
    essential_files,
    rlang_symbolic_links,
    rlang_files,
    prj_slug,
    rlang_deps,
):
    result = cookies.bake(
        extra_context={
            "project_name": "Test Project-CI/CD-3",
            "r_ver": "4.4",
        }
    )
    check_bake_result(result, 3)
    env_name = f"mamba_{result.project_path.name.lower()}"
    try:
        minimal_tests(
            result,
            essential_chs,
            essential_deps + rlang_deps,
            essential_files + rlang_files,
            rlang_symbolic_links,
            prj_slug,
        )

        print("===== #10. Checking R Kernel =====")
        path = result.project_path.name
        kernel_name = f"{path.lower()}_r"
        try:
            check_cmd = [get_project_jupyter(result.project_path), "kernelspec", "list"]
            res = subprocess.run(
                check_cmd, cwd=result.project_path, capture_output=True, text=True
            )
            assert (
                res.returncode == 0
            ), f"FAILED in #10! Failed to list Jupyter kernels:\n{res.stderr}"
            assert (
                kernel_name in res.stdout.lower()
            ), f"FAILED in #10! '{kernel_name}' not found in:\n{res.stdout}"
        finally:
            uninstall_kernel(kernel_name, result.project_path)
    finally:
        subprocess.run(
            ["mamba", "env", "remove", "-n", env_name, "-y"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def test_correct_template_is_reproducible(
    cookies, essential_chs, essential_deps, essential_files, symbolic_links, prj_slug
):
    result = cookies.bake(extra_context={"project_name": "Test Project-CI/CD-4"})

    check_bake_result(result, 4)

    project_path = result.project_path
    project_name = project_path.name
    env_name = f"mamba_{project_name.lower()}"
    kernel_name = f"{project_name.lower()}_py"
    clone_root = project_path.parent / "clone"
    clone_path = clone_root / project_name
    clone_root.mkdir()

    try:
        print("===== Removing side effects from fresh initialization =====")
        uninstall_kernel(kernel_name, project_path)

        subprocess.run(
            ["git", "add", "-A"],
            cwd=project_path,
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=BasalCell-CI",
                "-c",
                "user.email=ci@example.com",
                "commit",
                "--no-verify",
                "-m",
                "Test clone reproducibility",
            ],
            cwd=project_path,
            check=True,
        )

        subprocess.run(
            ["mamba", "env", "remove", "-n", env_name, "-y"],
            check=True,
        )

        print("===== Cloning project from committed repository state =====")
        subprocess.run(
            [
                "git",
                "clone",
                "--no-local",
                str(project_path),
                str(clone_path),
            ],
            check=True,
        )
        assert (
            clone_path / ".basalcell" / "conda-lock.yml"
        ).exists(), "FAILED! conda-lock.yml was not preserved through git clone"
        assert (
            clone_path / "poetry.lock"
        ).exists(), "FAILED! poetry.lock was not preserved through git clone"

        print("===== Reconstructing project from cloned repository =====")
        subprocess.run(
            ["make", "init"],
            cwd=clone_path,
            check=True,
        )

        print("===== Checking reconstructed project =====")
        minimal_project_tests(
            clone_path,
            project_name,
            essential_chs,
            essential_deps,
            essential_files,
            symbolic_links,
            prj_slug,
        )

        precommit_hook = clone_path / ".git" / "hooks" / "pre-commit"
        assert (
            precommit_hook.exists()
        ), "FAILED! pre-commit hook was not installed in the cloned repository"

    finally:
        subprocess.run(
            ["mamba", "env", "remove", "-n", env_name, "-y"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
