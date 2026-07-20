"""
Data loading utilities for the portfolio optimizer project.

Tomorrow's first task: fill in fetch_prices() and get comfortable with
what the returned DataFrame looks like before you touch any math.
"""

import pandas as pd
import yfinance as yf


def fetch_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """
    Download adjusted close prices for a list of tickers.

    Args:
        tickers: e.g. ["AAPL", "MSFT", "GOOGL", "SPY"]
        start: "YYYY-MM-DD"
        end: "YYYY-MM-DD"

    Returns:
        DataFrame indexed by date, one column per ticker.
    """
    # TODO: use yf.download(tickers, start=start, end=end)["Close"]
    raise NotImplementedError


def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Convert a price DataFrame into daily percentage returns.
    """
    # TODO: prices.pct_change().dropna()
    raise NotImplementedError


def compute_covariance(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Annualized covariance matrix from daily returns.
    Hint: daily_cov * 252 trading days.
    """
    # TODO
    raise NotImplementedError
