from datetime import datetime
from typing import Tuple

from ._path import PROJECT_ROOT
from ._query import query, query_essentials
from ._read import read_database

implemented_extensions = {
    "csv": "csv",
    "ipc": "ipc",
    "feather": "ipc",
    "pq": "parquet",
    "parquet": "parquet",
}


def extension_checker(extension: str) -> Tuple[str, str]:
    assert isinstance(
        extension, str
    ), f"extension should be str; got {extension}[{type(extension)}]"
    assert (
        extension in implemented_extensions
    ), f"extension should be either of {list(implemented_extensions)}, got {extension}"
    output_file_path = PROJECT_ROOT / f"{{cookiecutter.__project_slug}}_dependencies.{extension}"
    return output_file_path, implemented_extensions[extension]


def export_all_dependencies(extension: str = "csv") -> None:
    path, fmt = extension_checker(extension)
    getattr(read_database(), f"write_{fmt}")(path)


def export_essentials(extension: str = "csv") -> None:
    path, fmt = extension_checker(extension)
    getattr(query_essentials(), f"write_{fmt}")(path)


def export(*args) -> None:
    if args and args[-1] in implemented_extensions:
        extension = args[-1]
        keys = list(args[:-1])
    else:
        extension = "csv"
        keys = list(args)

    path, fmt = extension_checker(extension)
    getattr(query(key=keys), f"write_{fmt}")(path)


def report(*args) -> None:
    if not args or args[0] == "core":
        df = query_essentials()
    elif args[0] == "all":
        df = read_database()
    else:
        df = query(key=list(args))

    now_str = datetime.now().strftime("%H:%M:%S, %b %d, %Y")
    lines = [
        "# {{cookiecutter.project_name}}",
        "## Dependency Info",
        f"- this file was generated at: {now_str}",
        "",
    ]

    cols = df.columns
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "|".join([":---:"] * len(cols)) + "|")

    for row in df.iter_rows():
        safe_row = [str(val).replace("|", "&#124;") for val in row]
        lines.append("| " + " | ".join(safe_row) + " |")

    output_path = PROJECT_ROOT / "{{cookiecutter.__project_slug}}_dependencies.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
