"""
Test for BasalCell template generation
"""

import pytest
import subprocess


@pytest.fixture
def essential_files():
    return [
        ".gitignore",
        ".pre-commit-config.yaml",
        ".readthedocs.yaml",
        "launch_jupyter.py",
        "Makefile",
        "pyproject.toml",
        "README.md",
        ".github/workflows/test.yml",
        ".github/pull_request_template.md",
        "data/.gitkeep",
        "docs/_static/default_logo.png",
        "docs/jupyternb/output/.gitkeep",
        "docs/conf.py",
        "docs/index.md",
        "tests/__init__.py",
        "tools/__init__.py"
    ]


@pytest.fixture
def symbolic_links():
    return [
        "docs/jupyternb/data",
        "docs/jupyternb/tools",
    ]

@pytest.fixture
def rlang_files():
    return [
        "setup_r_env.sh",
        "renv.lock",
        ".Rprofile",
        "renv/activate.R",
        "renv/settings.json"
    ]


def uninstall_kernel(name, cwd):
    uninstall_cmd = ["poetry", "run", "jupyter", "kernelspec", "uninstall", "-y", name]
    subprocess.run(uninstall_cmd, cwd=cwd, capture_output=True, text=True)


def minimal_tests(result, fixture_essential_files, fixture_symbolic_links):
    print("===== #1. Checking exit code =====")
    assert result.exit_code == 0, \
        f"FAILED in #1! Invalid exit_code; expected 0, got {result.exit_code}"

    print("===== #2. Checking exception status =====")
    assert result.exception is None, \
        f"FAILED in #2! Invalid exception; expected None, got {result.exception}"

    print("===== #3. Checking project path name =====")
    assert result.project_path.name == "Test_Project_CI_CD", \
        f"FAILED in #3! Invalid path; expected `Test_Project_CI_CD`, got {result.project_path.name}"

    print("===== #4. Checking project path is a directory =====")
    assert result.project_path.is_dir(), \
        f"FAILED in #4! {result.project_path.name} is not a directory"

    print("===== #5. Checking essential files =====")
    for i, file in enumerate(fixture_essential_files):
        file_path = result.project_path / file
        assert file_path.exists(), \
            f"FAILED in #5-{i + 1}! {file} is not found in {result.project_path.name}"

    print("===== #6–8. Checking symbolic links =====")
    for i, link in enumerate(fixture_symbolic_links):
        link_path = result.project_path / link
        expected_target_name = link.split("/")[-1]
        resolved_path = link_path.resolve()
        # #6. If it's a symbolic link?
        assert link_path.is_symlink(), \
            f"FAILED in #6-{i + 1}! {link} is not a symbolic link"
        # #7. if it's not broken
        assert link_path.exists(), \
            f"FAILED in #7-{i + 1}! Symbolic link {link} is broken (target does not exist)"
        # #8. If it's referring to the correct path
        assert resolved_path.name == expected_target_name, \
            f"FAILED in #8-{i + 1}! {link} points to wrong target: {resolved_path.name}"

    print("===== #9. Checking Jupyter Kernel =====")
    expected_kernel_name = f"{result.project_path.name.lower()}_py"
    try:
        check_cmd = ["poetry", "run", "jupyter", "kernelspec", "list"]
        res = subprocess.run(check_cmd, cwd=result.project_path, capture_output=True, text=True)
        assert expected_kernel_name in res.stdout.lower(), \
            f"FAILED in #9! Kernel '{expected_kernel_name}' not found.\nAvailable kernels:\n{res.stdout}"
    finally:
        uninstall_kernel(expected_kernel_name, result.project_path)


def test_correct_template(cookies, essential_files, symbolic_links):
    result = cookies.bake(extra_context={"project_name": "Test Project-CI/CD"})
    minimal_tests(result, essential_files, symbolic_links)


def test_correct_template_for_package_mode(cookies, essential_files, symbolic_links):
    result = cookies.bake(
        extra_context={
            "project_name": "Test Project-CI/CD",
            "author_name": "John Smith",
            "email": "example@example.com",
            "create_package": "true"
        }
    )

    minimal_tests(result, essential_files, symbolic_links)

    print("===== #10. Checking Package files =====")
    project_slug = result.project_path.name.lower()
    file = f"src/{project_slug}/__init__.py"
    file_path = result.project_path / file
    assert file_path.exists(), \
        f"FAILED in #10! {file} is not found in {result.project_path.name}"


def test_correct_template_with_rlang(cookies, essential_files, symbolic_links, rlang_files):
    result = cookies.bake(
        extra_context={
            "project_name": "Test Project-CI/CD",
            "r_ver": "4.3"
        }
    )

    minimal_tests(result, essential_files, symbolic_links)

    print("===== #10. Checking R files =====")
    for i, file in enumerate(rlang_files):
        file_path = result.project_path / file
        assert file_path.exists(), \
            f"FAILED in #10-{i + 1}! {file} is not found in {result.project_path.name}"

    print("===== #11. Checking R Kernel =====")
    expected_kernel_name = f"{result.project_path.name.lower()}_r"
    try:
        check_cmd = ["poetry", "run", "jupyter", "kernelspec", "list"]
        res = subprocess.run(check_cmd, cwd=result.project_path, capture_output=True, text=True)
        assert expected_kernel_name in res.stdout.lower(), \
            f"FAILED in #11! Kernel '{expected_kernel_name}' not found.\nAvailable kernels:\n{res.stdout}"
    finally:
        uninstall_kernel(expected_kernel_name, result.project_path)
