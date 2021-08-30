"""Utilities for analyzing sales prices."""

from pathlib import Path
from datetime import datetime

import pandas


def read_prices(path: str) -> pandas.DataFrame:
    """Read sales csv."""
    return pandas.read_csv(path, parse_dates=['date'])


def count_sales_year(df: pandas.DataFrame) -> pandas.Series:
    """Count rows per sales year."""
    return df.date.dt.year.value_counts().sort_index(ascending=False)


def filter_sales_year(
    df: pandas.DataFrame,
    min_sales_year: int = 0,
    max_sales_year: int = datetime.today().year + 1
) -> pandas.DataFrame:
    """Filter sales by sales year."""
    idx = (df.date > str(min_sales_year)) & (df.date < str(max_sales_year))
    return df[idx]


def filter_build_year(
    df: pandas.DataFrame,
    min_build_year: int = 0,
    max_build_year: int = datetime.today().year + 1
) -> pandas.DataFrame:
    """Filter sales by build year."""
    return df[(df.built > min_build_year) & (df.built < max_build_year)]
