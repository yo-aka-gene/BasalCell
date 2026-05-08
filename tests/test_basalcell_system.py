import io
import os
import subprocess

import polars as pl
import pytest

prj_config = {"project_name": "testprj"}

ext_dict = [
    ("", "csv"),
    ("csv", "csv"),
    ("ipc", "ipc"),
    ("feather", "ipc"),
    ("pq", "pq"),
    ("parquet", "pq"),
]


def _format_determinant(s: str) -> bool:
    return not s.startswith("_") and s != ""


@pytest.fixture
def create_project(cookies, monkeypatch):
    def _create_project(extra_context) -> tuple:
        monkeypatch.delenv("CONDA_PREFIX", raising=False)
        monkeypatch.delenv("CONDA_DEFAULT_ENV", raising=False)
        monkeypatch.delenv("CONDA_PROMPT_MODIFIER", raising=False)
        monkeypatch.delenv("VIRTUAL_ENV", raising=False)
        monkeypatch.delenv("POETRY_ACTIVE", raising=False)
        result = cookies.bake(extra_context=extra_context)
        path = str(result.project_path)
        env = os.environ.copy()
        return path, env

    return _create_project


def read_markdown(filename: str) -> pl.DataFrame:
    with open(filename, "r") as f:
        lines = f.readlines()
    table_lines = [line.strip() for line in lines if line.startswith("|")]
    df = pl.read_csv(
        io.StringIO("\n".join(table_lines)),
        separator="|",
        has_header=True,
        skip_rows_after_header=1,
    )
    return df.select(
        [
            pl.col(c).alias(c.replace(" ", ""))
            for c in df.columns
            if _format_determinant(c)
        ]
    ).select(pl.all().str.strip_chars())


@pytest.mark.parametrize("ext", ext_dict)
def test_make_dump_all(create_project, ext):
    path, env = create_project(prj_config)
    ext, extension = ext

    ext_cmd = f"EXT={ext}" if ext != "" else ""

    subprocess.run(
        f"make dump-all {ext_cmd}",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    filename = "testprj_dependencies"
    filepath = os.path.join(path, f"{filename}.{extension}")
    assert os.path.exists(
        filepath
    ), f"FAILED in #1-1-1! {filename}.{extension} was not created for "
    f"dump-all EXT={ext}"

    df = getattr(pl, f"read_{extension if extension != 'pq' else 'parquet'}")(filepath)
    cols = [
        "name",
        "alias",
        "version",
        "required_version",
        "language",
        "platform",
        "installation",
    ]
    pkgs = df["name"].to_list()

    assert (
        df.columns == cols
    ), f"FAILED in #1-1-2! {filename}.{extension} for dump-all EXT={ext} "
    f"has invalid columns: {df.columns}"
    assert (
        "python" in pkgs
    ), f"FAILED in #1-1-3! {filename}.{extension} for dump-all EXT={ext} "
    f"does not include python info: {pkgs}"

    os.remove(filepath)


@pytest.mark.parametrize("ext", ext_dict)
def test_make_dump_core(create_project, ext):
    path, env = create_project(prj_config)
    ext, extension = ext

    ext_cmd = f"EXT={ext}" if ext != "" else ""

    subprocess.run(
        f"make add-py PKG=numpy && make lock && make dump-core {ext_cmd}",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    filename = "testprj_dependencies"
    filepath = os.path.join(path, f"{filename}.{extension}")
    assert os.path.exists(
        filepath
    ), f"FAILED in #1-2-1! {filename}.{extension} was not created for "
    f"dump-core EXT={ext}"

    df = getattr(pl, f"read_{extension if extension != 'pq' else 'parquet'}")(filepath)
    cols = [
        "name",
        "alias",
        "version",
        "required_version",
        "language",
        "platform",
        "installation",
    ]
    pkgs = df["name"].to_list()

    assert (
        df.columns == cols
    ), f"FAILED in #1-2-2! {filename}.{extension} for dump-core EXT={ext} "
    f"has invalid columns: {df.columns}"
    assert (
        "python" in pkgs
    ), f"FAILED in #1-2-3! {filename}.{extension} for dump-core EXT={ext} "
    f"does not include python info: {pkgs}"
    assert (
        "numpy" in pkgs
    ), f"FAILED in #1-2-4! {filename}.{extension} for dump-core EXT={ext} "
    "does not include added pkg info: "
    f"expected to have numpy in {pkgs}"

    os.remove(os.path.join(path, f"{filename}.{extension}"))


@pytest.mark.parametrize("ext", ext_dict)
def test_make_dump(create_project, ext):
    path, env = create_project(prj_config)
    ext, extension = ext

    ext_cmd = f"EXT={ext}" if ext != "" else ""

    subprocess.run(
        f"make add-py PKG=numpy && make lock && make dump KEYS=numpy {ext_cmd}",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    filename = "testprj_dependencies"
    filepath = os.path.join(path, f"{filename}.{extension}")
    assert os.path.exists(
        filepath
    ), f"FAILED in #1-3-1! {filename}.{extension} was not created for "
    f"dump KEY=numpy EXT={ext}"

    df = getattr(pl, f"read_{extension if extension != 'pq' else 'parquet'}")(filepath)
    cols = [
        "name",
        "alias",
        "version",
        "required_version",
        "language",
        "platform",
        "installation",
    ]
    pkgs = df["name"].to_list()

    assert (
        df.columns == cols
    ), f"FAILED in #1-3-2! {filename}.{extension} for dump KEY=numpy EXT={ext} "
    f"has invalid columns: {df.columns}"
    assert [
        "numpy"
    ] == pkgs, f"FAILED in #1-3-3! {filename}.{extension} for dump KEY=numpy EXT={ext} "
    f"is expected to have querried pkg info: got {pkgs}"

    os.remove(filepath)


def test_make_report_all(create_project):
    path, env = create_project(prj_config)

    subprocess.run(
        "make report KEYS=all",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    filename = "testprj_dependencies"
    filepath = os.path.join(path, f"{filename}.md")
    assert os.path.exists(
        filepath
    ), f"FAILED in #2-1-1! {filename}.md was not created for report KEYS=all"

    df = read_markdown(filepath)
    cols = [
        "name",
        "alias",
        "version",
        "required_version",
        "language",
        "platform",
        "installation",
    ]
    pkgs = df["name"].to_list()

    assert (
        df.columns == cols
    ), f"FAILED in #2-1-2! {filename}.md for report KEYS=all has invalid columns: "
    f"{df.columns}"
    assert (
        "python" in pkgs
    ), f"FAILED in #2-1-3! {filename}.md for report KEYS=all does not "
    f"include python info: {pkgs}"

    os.remove(filepath)


def test_make_report_core(create_project):
    path, env = create_project(prj_config)

    subprocess.run(
        "make add-py PKG=numpy && make lock && make report KEYS=core",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    filename = "testprj_dependencies"
    filepath = os.path.join(path, f"{filename}.md")
    assert os.path.exists(
        filepath
    ), f"FAILED in #2-2-1! {filename}.md was not created for report KEYS=core"

    df = read_markdown(filepath)
    cols = [
        "name",
        "alias",
        "version",
        "required_version",
        "language",
        "platform",
        "installation",
    ]
    pkgs = df["name"].to_list()

    assert (
        df.columns == cols
    ), f"FAILED in #2-2-2! {filename}.md for report KEYS=core has invalid columns: "
    f"{df.columns}"
    assert (
        "python" in pkgs
    ), f"FAILED in #2-2-3! {filename}.md for report KEYS=core does not "
    f"include python info: {pkgs}"
    assert (
        "numpy" in pkgs
    ), f"FAILED in #2-2-4! {filename}.md for report KEYS=core does not "
    "include added pkg info: "
    f"expected to have numpy in {pkgs}"

    os.remove(filepath)


def test_make_report_query(create_project):
    path, env = create_project(prj_config)

    subprocess.run(
        "make add-py PKG=numpy && make lock && make report KEYS=numpy",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    filename = "testprj_dependencies"
    filepath = os.path.join(path, f"{filename}.md")
    assert os.path.exists(
        filepath
    ), f"FAILED in #2-3-1! {filename}.md was not created for report KEYS=numpy"

    df = read_markdown(filepath)
    cols = [
        "name",
        "alias",
        "version",
        "required_version",
        "language",
        "platform",
        "installation",
    ]
    pkgs = df["name"].to_list()

    assert (
        df.columns == cols
    ), f"FAILED in #2-3-2! {filename}.md for report KEYS=numpy has invalid columns: "
    f"{df.columns}"
    assert [
        "numpy"
    ] == pkgs, f"FAILED in #2-3-3! {filename}.md for report KEYS=numpy is "
    f"expected to have querried pkg info: got {pkgs}"

    os.remove(filepath)


def test_make_report(create_project):
    path, env = create_project(prj_config)

    subprocess.run(
        "make add-py PKG=numpy && make lock && make report",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    filename = "testprj_dependencies"
    filepath = os.path.join(path, f"{filename}.md")
    assert os.path.exists(
        filepath
    ), f"FAILED in #2-4-1! {filename}.md was not created for report KEY="

    df = read_markdown(filepath)
    cols = [
        "name",
        "alias",
        "version",
        "required_version",
        "language",
        "platform",
        "installation",
    ]
    pkgs = df["name"].to_list()

    assert (
        df.columns == cols
    ), f"FAILED in #2-4-2! {filename}.md for report KEY= has invalid columns: "
    f"{df.columns}"
    assert (
        "python" in pkgs
    ), f"FAILED in #2-4-3! {filename}.md for report KEY= does not include python info: "
    f"{pkgs}"
    assert "numpy" in pkgs, f"FAILED in #2-4-4! {filename}.md "
    "for report KEY= does not include added pkg info: "
    f"expected to have numpy in {pkgs}"

    os.remove(filepath)
