"""
Data loading utilities for the portfolio optimizer project.

The whole pipeline starts here and is only three ideas:

    prices  --->  daily returns  --->  covariance (risk)

Everything the optimizer does later is built on top of these three
functions, so it is worth being able to explain each one in a sentence:

    fetch_prices          -> download a table of daily prices
    compute_daily_returns -> turn prices into daily % changes
    compute_covariance    -> measure how the assets move together (risk)
"""

import os

import pandas as pd
import yfinance as yf


def fetch_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """
    Download daily (split/dividend-adjusted) closing prices.

    Args:
        tickers: e.g. ["AAPL", "MSFT", "GOOGL", "SPY"]
        start: "YYYY-MM-DD"
        end: "YYYY-MM-DD"

    Returns:
        DataFrame indexed by date, one column per ticker.

    Note on "adjusted" prices:
        yfinance defaults to auto_adjust=True, which means the "Close"
        column is ALREADY adjusted for stock splits and dividends. That
        is exactly what we want for return calculations, so we do not
        need a separate "Adj Close" column. We pass auto_adjust=True
        explicitly here so the behavior is obvious and does not silently
        change if yfinance's defaults ever change.
    """
    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True,   # "Close" comes back already adjusted
        progress=False,     # don't print a download bar
    )

    # With a list of tickers, yfinance returns a table whose columns are
    # grouped by field ("Close", "Open", "High", ...). We only want Close.
    prices = data["Close"]

    # If a single ticker was passed as a plain string, yfinance may hand
    # back a Series instead of a one-column table. Normalize to a table.
    if isinstance(prices, pd.Series):
        name = tickers if isinstance(tickers, str) else tickers[0]
        prices = prices.to_frame(name=name)

    return prices


def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Convert a price table into daily percentage returns.

    pct_change() compares each day to the previous day:
        (today - yesterday) / yesterday
    The very first day has no "previous" day, so it comes out blank (NaN);
    dropna() removes that first empty row.
    """
    return prices.pct_change().dropna()


def compute_covariance(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Annualized covariance matrix from daily returns.

    Covariance measures how two assets move together. The raw number from
    .cov() is a *daily* figure; multiplying by 252 (roughly the number of
    trading days in a year) scales it up to an annual figure, which is the
    convention everyone in finance uses.
    """
    return returns.cov() * 252


def load_prices_cached(
    tickers: list[str],
    start: str,
    end: str,
    cache_path: str = "data/prices.csv",
) -> pd.DataFrame:
    """
    Return prices, downloading them only the first time.

    The idea ("pull once, compute forever"):
        - If the cache file already exists, just read it (instant, offline).
        - Otherwise download from yfinance and save it for next time.

    To force a fresh download later, simply delete the cache file.
    """
    if os.path.exists(cache_path):
        # index_col=0 -> the first column (the dates) becomes the row labels
        # parse_dates=True -> read those labels as real dates, not text
        return pd.read_csv(cache_path, index_col=0, parse_dates=True)

    prices = fetch_prices(tickers, start, end)

    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    prices.to_csv(cache_path)
    return prices
