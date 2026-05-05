from typing import List

import polars as pl

from ._read import predetermined_pkg_groups, read_database, read_lookup


def resolve(key: List[str]) -> List[str]:
    return read_lookup().filter(pl.col("query").is_in(key)).collect()["name"].to_list()


def query(key: List[str]) -> pl.LazyFrame:
    return read_database().filter(pl.col("name").is_in(resolve(key)))


def query_essentials() -> pl.LazyFrame:
    master = predetermined_pkg_groups()
    key = master["env"] + master["pypkgs"]
{%- if cookiecutter.r_ver != "none" %}
    devs = master["pydevs"] + master["rdevs"]
{%- else %}
    devs = master["pydevs"]
{%- endif %}
    return read_database().filter(
        (pl.col("name").is_in(key))
        & (~pl.col("name").is_in(devs))
        & (pl.col("language") != "System")
    )
