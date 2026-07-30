"""
Portfolio scoring functions: turn a set of weights into return, risk, Sharpe.

Think of these as the *scoreboard*. They don't decide anything -- they just
measure how good a given allocation is. Both the Markowitz baseline and
(later) the PSO swarm will score their candidate portfolios with these.

Convention: inputs are already ANNUAL.
    mean_returns_annual = daily_returns.mean() * 252
    cov_annual          = daily_returns.cov()  * 252
"""

import numpy as np


def portfolio_return(weights, mean_returns_annual) -> float:
    """
    The portfolio's yearly return = weighted average of each holding's return.

    Example: 50% in a 10% stock + 50% in a 20% stock -> 15%.
    """
    weights = np.asarray(weights)
    mean_returns_annual = np.asarray(mean_returns_annual)
    return float(weights @ mean_returns_annual)


def portfolio_volatility(weights, cov_annual) -> float:
    """
    The portfolio's yearly risk (volatility).

    This is NOT the average of the individual risks. It uses the whole
    covariance matrix, so it accounts for how the holdings move together --
    which is exactly where diversification lowers the number.

    The math (w . Cov . w) is: for every pair of holdings, multiply
    (how much you hold of each) x (how much they jump / co-jump), and add
    it all up. Then square-root to get back into normal % units.
    """
    weights = np.asarray(weights)
    cov_annual = np.asarray(cov_annual)
    variance = weights @ cov_annual @ weights
    return float(np.sqrt(variance))


def sharpe_ratio(weights, mean_returns_annual, cov_annual, risk_free=0.04) -> float:
    """
    Reward per unit of risk: (return - safe rate) / risk. Higher = better deal.
    """
    r = portfolio_return(weights, mean_returns_annual)
    v = portfolio_volatility(weights, cov_annual)
    return (r - risk_free) / v
