"""
Markowitz mean-variance baseline (the classical approach).

This uses a math solver (scipy) to find the weights with the best score,
subject to two SIMPLE rules:
    - all weights add up to 1        (invest 100% of the money)
    - every weight >= 0              (long-only: no short selling)

With only these simple rules the problem is "convex" -- meaning it has one
clear best answer and the solver finds it instantly and reliably.

This is the benchmark the PSO swarm must MATCH here on the easy case... and
the method that BREAKS once we add hard real-world rules (max 8 holdings,
minimum position sizes), which is where PSO earns its place.
"""

import numpy as np
from scipy.optimize import minimize

from src.metrics import portfolio_volatility, sharpe_ratio


def _base_constraints(n):
    """The two simple rules, in the format scipy expects."""
    bounds = tuple((0.0, 1.0) for _ in range(n))                 # long-only
    weights_sum_to_one = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
    return bounds, [weights_sum_to_one]


def max_sharpe_portfolio(mean_returns_annual, cov_annual, risk_free=0.04):
    """
    Find the weights with the HIGHEST Sharpe ratio (the best-deal portfolio).

    scipy only knows how to MINIMIZE, so to maximize Sharpe we minimize its
    negative. That's the only trick here.
    """
    n = len(mean_returns_annual)
    bounds, constraints = _base_constraints(n)
    start = np.repeat(1.0 / n, n)  # start from the equal-weight guess

    result = minimize(
        lambda w: -sharpe_ratio(w, mean_returns_annual, cov_annual, risk_free),
        start,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )
    return result.x


def min_volatility_portfolio(cov_annual):
    """Find the weights with the LOWEST possible risk (the calmest portfolio)."""
    n = cov_annual.shape[0]
    bounds, constraints = _base_constraints(n)
    start = np.repeat(1.0 / n, n)

    result = minimize(
        lambda w: portfolio_volatility(w, cov_annual),
        start,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )
    return result.x


def equal_weight_portfolio(n):
    """The naive 'split evenly' portfolio -- our sanity-check benchmark."""
    return np.repeat(1.0 / n, n)
