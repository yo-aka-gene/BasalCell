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
def test_make_dump_all(cookies, ext):
    result = cookies.bake(extra_context=prj_config)
    path = str(result.project_path)
    ext, extension = ext

    ext_cmd = f"EXT={ext}" if ext != "" else ""

    dump_all = subprocess.run(
        f"make dump-all {ext_cmd}",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    if dump_all.exit_code != 0:
        raise dump_all.exception

    filename = "testprj_dependencies"
    assert os.path.exists(
        os.path.join(path, f"{filename}.{extension}")
    ), f"FAILED in #1-1-1! {filename}.{extension} was not created for "
    f"dump-all EXT={ext}"

    df = getattr(pl, f"read_{extension}")(f"{filename}.{extension}")
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

    os.remove(os.path.join(path, f"{filename}.{extension}"))


@pytest.mark.parametrize("ext", ext_dict)
def test_make_dump_core(cookies, ext):
    result = cookies.bake(extra_context=prj_config)
    path = str(result.project_path)
    ext, extension = ext

    ext_cmd = f"EXT={ext}" if ext != "" else ""

    dump_core = subprocess.run(
        "make add-py PKG=numpy && " "make lock && " f"make dump-core {ext_cmd}",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    if dump_core.exit_code != 0:
        raise dump_core.exception

    filename = "testprj_dependencies"
    assert os.path.exists(
        os.path.join(path, f"{filename}.{extension}")
    ), f"FAILED in #1-2-1! {filename}.{extension} was not created for "
    f"dump-core EXT={ext}"

    df = getattr(pl, f"read_{extension}")(f"{filename}.{extension}")
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
def test_make_dump(cookies, ext):
    result = cookies.bake(extra_context=prj_config)
    path = str(result.project_path)
    ext, extension = ext

    ext_cmd = f"EXT={ext}" if ext != "" else ""

    dump = subprocess.run(
        "make add-py PKG=numpy && " "make lock && " f"make dump KEYS=numpy {ext_cmd}",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    if dump.exit_code != 0:
        raise dump.exception

    filename = "testprj_dependencies"
    assert os.path.exists(
        os.path.join(path, f"{filename}.{extension}")
    ), f"FAILED in #1-3-1! {filename}.{extension} was not created for "
    f"dump KEY=numpy EXT={ext}"

    df = getattr(pl, f"read_{extension}")(f"{filename}.{extension}")
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

    os.remove(os.path.join(path, f"{filename}.{extension}"))


def test_make_report_all(cookies):
    result = cookies.bake(extra_context=prj_config)
    path = str(result.project_path)

    dump_all = subprocess.run(
        "make report KEYS=all",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    if dump_all.exit_code != 0:
        raise dump_all.exception

    filename = "testprj_dependencies"
    assert os.path.exists(
        os.path.join(path, f"{filename}.md")
    ), f"FAILED in #2-1-1! {filename}.md was not created for report KEYS=all"

    df = read_markdown(f"{filename}.md")
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

    os.remove(os.path.join(path, f"{filename}.md"))


def test_make_report_core(cookies):
    result = cookies.bake(extra_context=prj_config)
    path = str(result.project_path)

    dump_all = subprocess.run(
        "make add-py PKG=numpy && " "make lock && " "make report KEYS=core",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    if dump_all.exit_code != 0:
        raise dump_all.exception

    filename = "testprj_dependencies"
    assert os.path.exists(
        os.path.join(path, f"{filename}.md")
    ), f"FAILED in #2-2-1! {filename}.md was not created for report KEYS=core"

    df = read_markdown(f"{filename}.md")
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

    os.remove(os.path.join(path, f"{filename}.md"))


def test_make_report_query(cookies):
    result = cookies.bake(extra_context=prj_config)
    path = str(result.project_path)

    dump_all = subprocess.run(
        "make add-py PKG=numpy && " "make lock && " "make report KEYS=numpy",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    if dump_all.exit_code != 0:
        raise dump_all.exception

    filename = "testprj_dependencies"
    assert os.path.exists(
        os.path.join(path, f"{filename}.md")
    ), f"FAILED in #2-3-1! {filename}.md was not created for report KEYS=numpy"

    df = read_markdown(f"{filename}.md")
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

    os.remove(os.path.join(path, f"{filename}.md"))


def test_make_report(cookies):
    result = cookies.bake(extra_context=prj_config)
    path = str(result.project_path)

    dump_all = subprocess.run(
        "make add-py PKG=numpy && make lock && make report",
        cwd=path,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    if dump_all.exit_code != 0:
        raise dump_all.exception

    filename = "testprj_dependencies"
    assert os.path.exists(
        os.path.join(path, f"{filename}.md")
    ), f"FAILED in #2-4-1! {filename}.md was not created for report KEY="

    df = read_markdown(f"{filename}.md")
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

    os.remove(os.path.join(path, f"{filename}.md"))
