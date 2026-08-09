"""
Walk-forward backtest for SwarmFolio.

Golden rule: at each step, decide weights using ONLY past data,
then earn the return that ACTUALLY happened next. Never peek at the future.
"""
import numpy as np
import pandas as pd


def backtest(returns, optimize_fn, lookback=252, rebalance_every=63, cost=0.001):
    n = len(returns)
    equity = 1.0            # start with $1
    curve, daily = [], []   # portfolio value over time, and daily returns
    weights = None
    prev_weights = None
    total_turnover = 0.0

    for t in range(lookback, n):
        # --- REBALANCE every `rebalance_every` days ---
        if (t - lookback) % rebalance_every == 0:
            past = returns.iloc[t-lookback:t]          
            mean = past.mean().values * 252
            cov = past.cov().values * 252
            weights = optimize_fn(mean, cov)
            if prev_weights is not None:
                turnover = np.abs(weights - prev_weights).sum()
                total_turnover += turnover
                equity *= (1 - cost * turnover)        # pay transaction cost when we trade
            prev_weights = weights

        # --- EARN today's ACTUAL return with the weights we already hold ---
        day_return = returns.iloc[t].values @ weights  # day t's real return
        equity *= (1 + day_return)
        curve.append(equity)
        daily.append(day_return)

    return pd.Series(curve, index=returns.index[lookback:]), np.array(daily), total_turnover

def backtest_metrics(curve, daily, risk_free=0.04):
    years = len(daily) / 252
    total_return  = curve.iloc[-1] - 1
    annual_return = curve.iloc[-1] ** (1 / years) - 1
    sharpe        = (daily.mean() * 252 - risk_free) / (daily.std() * np.sqrt(252))
    running_max   = np.maximum.accumulate(curve.values)
    max_drawdown  = ((curve.values - running_max) / running_max).min()
    return {
        "total_return":  total_return,
        "annual_return": annual_return,
        "sharpe":        sharpe,
        "max_drawdown":  max_drawdown,
    }