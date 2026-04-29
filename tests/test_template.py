"""
Test for BasalCell template generation
"""

import subprocess

import pytest


@pytest.fixture
def prj_slug():
    return "REPLACETHIS"


@pytest.fixture
def essential_files():
    return [
        ".gitignore",
        ".pre-commit-config.yaml",
        ".readthedocs.yaml",
        "environment.yml",
        "launch_jupyter.py",
        "Makefile",
        "pyproject.toml",
        "README.md",
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
def rlang_files():
    return [
        ".lintr",
        ".Renviron",
        "setup_r_env.sh",
        "renv.lock",
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


def uninstall_kernel(name, cwd):
    uninstall_cmd = ["poetry", "run", "jupyter", "kernelspec", "uninstall", "-y", name]
    subprocess.run(uninstall_cmd, cwd=cwd, capture_output=True, text=True)


def minimal_tests(result, fixture_essential_files, fixture_symbolic_links, slug, idx):
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

    print("===== #3. Checking project path name =====")
    path = result.project_path.name
    assert (
        path == f"Test_Project_CI_CD_{idx}"
    ), f"FAILED in #3! Invalid path; expected `Test_Project_CI_CD_{idx}`, got {path}"

    print("===== #4. Checking project path is a directory =====")
    assert result.project_path.is_dir(), f"FAILED in #4! {path} is not a directory"

    print("===== #5. Checking essential files =====")
    for i, file in enumerate(fixture_essential_files):
        file = (file).replace(slug, path.lower())
        file_path = result.project_path / file
        assert (
            file_path.exists()
        ), f"FAILED in #5-{i + 1}! {file} is not found in {path}"

    print("===== #6–8. Checking symbolic links =====")
    for i, link in enumerate(fixture_symbolic_links):
        link = (link).replace(slug, path.lower())
        link_path = result.project_path / link
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
    kernel_name = f"{path.lower()}_py"
    try:
        check_cmd = ["poetry", "run", "jupyter", "kernelspec", "list"]
        res = subprocess.run(
            check_cmd, cwd=result.project_path, capture_output=True, text=True
        )
        assert (
            kernel_name in res.stdout.lower()
        ), f"FAILED in #9! '{kernel_name}' not found in:\n{res.stdout}"
    finally:
        uninstall_kernel(kernel_name, result.project_path)


def test_correct_template(cookies, essential_files, symbolic_links, prj_slug):
    result = cookies.bake(extra_context={"project_name": "Test Project-CI/CD-1"})
    minimal_tests(result, essential_files, symbolic_links, prj_slug, 1)


def test_correct_template_for_package_mode(
    cookies, essential_files, symbolic_links, prj_slug
):
    result = cookies.bake(
        extra_context={
            "project_name": "Test Project-CI/CD-2",
            "author_name": "John Smith",
            "email": "example@example.com",
            "python_ver": "3.11",
            "create_package": "true",
        }
    )

    minimal_tests(result, essential_files, symbolic_links, prj_slug, 2)

    print("===== #10. Checking Package files =====")
    path = result.project_path.name
    project_slug = path.lower()
    file = f"src/{project_slug}/__init__.py"
    file_path = result.project_path / file
    assert file_path.exists(), f"FAILED in #10! {file} is not found in {path}"


def test_correct_template_with_rlang(
    cookies, essential_files, rlang_symbolic_links, rlang_files, prj_slug
):
    result = cookies.bake(
        extra_context={
            "project_name": "Test Project-CI/CD-3",
            "python_ver": "3.12",
            "r_ver": "4.4",
        }
    )

    minimal_tests(result, essential_files, rlang_symbolic_links, prj_slug, 3)

    print("===== #10. Checking R files =====")
    path = result.project_path.name
    for i, file in enumerate(rlang_files):
        file = (file).replace(prj_slug, path.lower())
        file_path = result.project_path / file
        assert (
            file_path.exists()
        ), f"FAILED in #10-{i + 1}! {file} is not found in {path}"

    print("===== #11. Checking R Kernel =====")
    kernel_name = f"{path.lower()}_r"
    try:
        check_cmd = ["poetry", "run", "jupyter", "kernelspec", "list"]
        res = subprocess.run(
            check_cmd, cwd=result.project_path, capture_output=True, text=True
        )
        assert (
            kernel_name in res.stdout.lower()
        ), f"FAILED in #11! '{kernel_name}' not found in:\n{res.stdout}"
    finally:
        uninstall_kernel(kernel_name, result.project_path)
