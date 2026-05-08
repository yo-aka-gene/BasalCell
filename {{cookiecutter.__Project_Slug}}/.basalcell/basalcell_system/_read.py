import json
from typing import Dict, List

import polars as pl
import yaml

from ._path import (
    CONDA_LOCK_YML,
    ENVIRONMENT_YML,
    POETRY_REQUIREMENTS_TXT,
    PYPROJECT_TOML,
{%- if cookiecutter.r_ver != "none" %}
    RENV_LOCK,
{%- endif %}
)

cols = [
    "name",
    "alias",
    "version",
    "required_version",
    "language",
    "platform",
    "installation",
]

# poetry
with open(POETRY_REQUIREMENTS_TXT, "r") as f:
    requirements = [v.split(" ; ")[0] for v in f.readlines()]
    txt_pkg = [v.split("==")[0] for v in requirements]
    txt_ver = [v.split("==")[1] for v in requirements]


with open(PYPROJECT_TOML, "r") as f:
    pyproject = f.readlines()

pyproject_pkgs = [
    v
    for v in "".join(
        [v for v in "".join(pyproject).split("[") if "dependencies" in v]
    ).split("\n")
    if " = " in v
]

pyproject_dev_pkgs = [
    v
    for v in "".join(
        [v for v in "".join(pyproject).split("[") if "dev.dependencies" in v]
    ).split("\n")
    if " = " in v
]
pypkgs = [v.split(" = ")[0] for v in pyproject_pkgs]
pydevs = [v.split(" = ")[0] for v in pyproject_dev_pkgs]


def read_poetry_df() -> pl.DataFrame:
    txt_based = pl.DataFrame(
        {
            "name": txt_pkg,
            "alias": txt_pkg,
            "version": txt_ver,
            "language": "Python",
            "platform": "any",
            "installation": "poetry",
        }
    )

    toml_based = (
        pl.DataFrame(
            {
                "name": pypkgs,
                "required_version": [
                    v.split(" = ")[1].replace('"', "") for v in pyproject_pkgs
                ],
            }
        )
        .unique("name", maintain_order=True)
    )

    return (
        txt_based.join(toml_based, on="name", how="left")
        .select(cols)
        .unique()
        .sort("name")
    )


# raw envionment.yml
with open(ENVIRONMENT_YML, "r") as f:
    env_yaml = yaml.safe_load(f)
env_pkgs = [
    {"_name": dep} for dep in env_yaml.get("dependencies", []) if isinstance(dep, str)
]
df_env = (
    pl.DataFrame(env_pkgs)
    .with_columns(
        pl.col("_name").str.extract(r"^([a-zA-Z0-9_\-\.]+)").alias("name"),
        pl.col("_name")
        .str.extract(r"([<>=~!]+.*)$")
        .str.strip_chars()
        .alias("required_version"),
    )
    .drop("_name")
)


# raw conda-lock.yml
with open(CONDA_LOCK_YML, "r") as f:
    conda_lock = yaml.safe_load(f)
lock_pkgs = []
for pkg in conda_lock.get("package", []):
    lock_pkgs.append(
        {
            "name": pkg.get("name"),
            "version": pkg.get("version"),
            "language": "System",
            "platform": pkg.get("platform"),
            "installation": "Mamba",
        }
    )
df_conda_lock = pl.DataFrame(lock_pkgs).with_columns(pl.col("version").cast(pl.String))
valid_mamba_names = df_conda_lock["name"].to_list()
{%- if cookiecutter.r_ver != "none" %}


# renv
with open(RENV_LOCK, "r") as f:
    renv_lock = json.load(f)
renv_pkgs = []
for pkg_name, pkg_info in renv_lock.get("Packages", {}).items():
    renv_pkgs.append(
        {"alias": pkg_name, "version": pkg_info.get("Version"), "language": "R"}
    )
df_renv = (
    pl.DataFrame(renv_pkgs)
    .with_columns(
        cand_r=pl.lit("r-") + pl.col("alias").str.to_lowercase(),
        cand_bioc=pl.lit("bioconductor-") + pl.col("alias").str.to_lowercase(),
        cand_backend=pl.lit("_r-") + pl.col("alias").str.to_lowercase(),
    )
    .with_columns(
        name_in_mamba=pl.when(pl.col("cand_r").is_in(valid_mamba_names))
        .then(pl.col("cand_r"))
        .when(pl.col("cand_bioc").is_in(valid_mamba_names))
        .then(pl.col("cand_bioc"))
        .when(pl.col("cand_backend").is_in(valid_mamba_names))
        .then(pl.col("cand_backend"))
        .otherwise(pl.lit(None))
    )
    .with_columns(
        installation=pl.when(pl.col("name_in_mamba").is_null())
        .then(pl.lit("renv"))
        .otherwise(pl.lit("Mamba")),
        name=pl.col("name_in_mamba").fill_null(pl.col("alias")),
        platform=pl.lit("any"),
    )
    .drop(["cand_r", "cand_bioc", "cand_backend", "name_in_mamba"])
    .join(df_env.unique("name"), on="name", how="left")
    .select(cols)
)


def read_renv_df() -> pl.DataFrame:
    return df_renv.sort("alias")


df_poetry = read_poetry_df()


df_os = (
    df_conda_lock.filter(
        (~pl.col("name").is_in(df_renv["name"].to_list()))
        & (~pl.col("name").is_in(df_poetry["name"].to_list()))
    )
    .with_columns(alias=pl.col("name"))
    .join(df_env.unique("name"), on="name", how="left")
    .select(cols)
    .with_columns(
        pl.when(pl.col("name") == "python")
        .then(pl.lit("Python"))
        .when(pl.col("name") == "r-base")
        .then(pl.lit("R"))
        .otherwise(pl.col("language"))
        .alias("language"),
        pl.when(pl.col("name") == "r-base")
        .then(pl.lit("R"))
        .otherwise(pl.col("alias"))
        .alias("alias"),
    )
)


def read_mamba_df() -> pl.DataFrame:
    return df_os.sort("name")


def read_database() -> pl.DataFrame:
    return pl.concat([read_poetry_df(), read_renv_df(), read_mamba_df()]).sort(
        ["language", "alias"]
    )
{%- else %}


df_poetry = read_poetry_df()


df_os = df_conda_lock.filter(
    (~pl.col("name").is_in(df_poetry["name"].to_list()))
).with_columns(alias=pl.col("name")).join(
    df_env.unique("name"), on="name", how="left"
).select(cols).with_columns(
    pl.when(pl.col("name") == "python").then(pl.lit("Python"))
    .otherwise(pl.col("language"))
    .alias("language")
)

def read_mamba_df() -> pl.DataFrame:
    return df_os.sort("name")


def read_database() -> pl.DataFrame:
    return pl.concat([
        read_poetry_df(),
        read_mamba_df()
    ]).sort(["language", "alias"])
{%- endif %}


def read_lookup() -> pl.DataFrame:
    return (
        read_database()
        .with_columns(pl.concat_list(["name", "alias"]).list.unique().alias("query"))
        .explode("query")
        .select("query", "name")
    )


def predetermined_pkg_groups() -> Dict[str, List[str]]:
    return {
        "env": df_env["name"].to_list(),
        "pypkgs": pypkgs,
        "pydevs": pydevs,
{%- if cookiecutter.r_ver != "none" %}
        "rdevs": [
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
        ],
{%- endif %}
    }
