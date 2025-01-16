"""Utilities for analyzing sales prices."""

import datetime
import pandas


def read_prices(path: str) -> pandas.DataFrame:
    """Read sales csv."""
    return pandas.read_csv(path, parse_dates=['date'], date_format='%d-%m-%Y')


def count_sales_year(df: pandas.DataFrame) -> pandas.Series:
    """Count rows per sales year."""
    return df.date.dt.year.value_counts().sort_index(ascending=False)


def filter_sales_year(
    df: pandas.DataFrame,
    min_sales_year: int = datetime.MINYEAR,
    max_sales_year: int = datetime.datetime.today().year
) -> pandas.DataFrame:
    """Filter sales by sales year."""
    min_sales_year = datetime.datetime(min_sales_year, 1, 1)
    max_sales_year = datetime.datetime(max_sales_year + 1, 1, 1)
    idx = (df.date > min_sales_year) & (df.date < max_sales_year)
    return df[idx]


def filter_build_year(
    df: pandas.DataFrame,
    min_build_year: int = 0,
    max_build_year: int = datetime.datetime.today().year
) -> pandas.DataFrame:
    """Filter sales by build year."""
    idx = (df.built > min_build_year - 1) & (df.built < max_build_year + 1)
    return df[idx]


def filter_area(df: pandas.DataFrame, min_area: int, max_area: int) -> pandas.DataFrame:
    idx = (df.m2 <= max_area) & (df.m2 >= min_area)
    return df[idx]


def predict_sales_price(prices: pandas.DataFrame, 
                        house_area: int,
                        min_sales_year: int = 1,
                        max_sales_year: int = datetime.datetime.today().year, 
                        min_area: int = 0, 
                        max_area: int = 9999,
                        min_samples: int = 0) -> float:
    prices = filter_sales_year(prices, min_sales_year, max_sales_year)
    prices = filter_area(prices, min_area, max_area)
    if len(prices) < min_samples:
        raise ValueError(f'Not enough samples to predict, need at least {min_samples} got {len(prices)}')
    return prices.m2_price.median() * house_area
