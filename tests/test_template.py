"""
Test for BasalCell template generation
"""

import pytest


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
def essential_symbolic_links():
    return [
        "docs/jupyternb/data",
        "docs/jupyternb/tools",
    ]


def test_correct_exit_code(cookies):
    result = cookies.bake(extra_context={"project_name": "Test Project"})
    assert result.exit_code == 0, \
        f"Invalid exit_code; expected 0, got {result.exit_code}"


def test_correct_exception(cookies):
    result = cookies.bake(extra_context={"project_name": "Test Project"})
    assert result.exception is None, \
        f"Invalid exception; expected None, got {result.exception}"


def test_correct_path_name(cookies):
    result = cookies.bake(extra_context={"project_name": "Test Project-7"})
    assert result.project_path.name == "test_project_7", \
        f"Invalid path; expected `test_project_7`, got {result.project_path.name}"


def test_is_directory(cookies):
    result = cookies.bake(extra_context={"project_name": "Test Project-7"})
    assert result.project_path.is_dir(), \
        f"{result.project_path.name} is not a directory"


def test_correct_exception(cookies):
    result = cookies.bake(extra_context={"project_name": "Test Project"})
    for file in essential_files():
        assert (result.project_path / file).exists(), \
            f"{file} is not found in {result.project_path.name}"
        

def test_essential_files_exist(cookies, essential_files):
    result = cookies.bake(extra_context={"project_name": "Test Project"})
    for file in essential_files:
        file_path = result.project_path / file
        assert file_path.exists(), \
            f"{file} is not found in {result.project_path.name}"


def test_symbolic_link_exists(cookies, essential_symbolic_links):
    result = cookies.bake(extra_context={"project_name": "Test Project"})
    for link in essential_symbolic_links:
        link_path = result.project_path / link
        assert link_path.is_symlink(), \
            f"{link} is not a symbolic link"


def test_valid_symbolic_link(cookies, essential_symbolic_links):
    result = cookies.bake(extra_context={"project_name": "Test Project"})
    for link in essential_symbolic_links:
        link_path = result.project_path / link
        assert link_path.exists(), \
            f"Symbolic link {link} is broken (target does not exist)"


def test_synbolic_link_for_correct_target(cookies, essential_symbolic_links):
    result = cookies.bake(extra_context={"project_name": "Test Project"})
    for link in essential_symbolic_links:
        link_path = result.project_path / link
        expected_target_name = link.split("/")[-1]
        resolved_path = link_path.resolve()
        assert resolved_path.name == expected_target_name, \
            f"{link} points to wrong target: {resolved_path.name}"
