"""
FastAPI backend: exposes the SwarmFolio engine to the React frontend.

- Loads the cached prices once at startup.
- Precomputes a walk-forward backtest once (fast Markowitz strategy) for the chart.
- POST /optimize runs the constrained PSO live for the given constraints.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.data_loader import load_prices_cached, compute_daily_returns, compute_covariance
from src.metrics import portfolio_return
from src.pso import optimize_portfolio
from src.baseline import max_sharpe_portfolio
from src.backtest import backtest, backtest_metrics

TICKERS = ["AAPL", "MSFT", "GOOGL", "NVDA", "AMZN", "META", "JPM", "GS", "BAC",
           "JNJ", "UNH", "PFE", "PG", "KO", "WMT", "XOM", "CVX", "GLD", "TLT", "SPY"]

app = FastAPI(title="SwarmFolio API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev: any origin (frontend on :5173)
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- load data + precompute the backtest once, at startup ----
_prices = load_prices_cached(TICKERS, "2015-01-01", "2026-07-01")
INVEST = [c for c in _prices.columns if c != "SPY"]
_rets = compute_daily_returns(_prices)
_inv = _rets[INVEST]
MEAN = (_inv.mean() * 252).values
COV = compute_covariance(_inv).values

_curve, _daily, _turn = backtest(_inv, max_sharpe_portfolio)
_bt = backtest_metrics(_curve, _daily)
_step = max(1, len(_curve) // 120)
EQUITY = [
    {"t": float(_curve.index[i].year) + _curve.index[i].month / 12.0,
     "value": round(float(_curve.iloc[i]), 3)}
    for i in range(0, len(_curve), _step)
]
BACKTEST_MAX_DD = float(_bt["max_drawdown"])


class OptimizeReq(BaseModel):
    max_holdings: int = 8
    min_weight: float = 0.05   # a fraction (e.g. 0.05 = 5%)
    min_holdings: int = 3


@app.get("/health")
def health():
    return {"ok": True, "assets": len(INVEST)}


@app.post("/optimize")
def optimize(req: OptimizeReq):
    res = optimize_portfolio(
        MEAN, COV,
        max_holdings=req.max_holdings,
        min_weight=req.min_weight,
        min_holdings=req.min_holdings,
    )
    w = res["weights"]
    holdings = sorted(
        [{"ticker": INVEST[i], "weight": float(w[i])} for i in range(len(w)) if w[i] > 0.01],
        key=lambda h: -h["weight"],
    )
    return {
        "feasible": bool(res["feasible"]),
        "violations": {k: float(v) for k, v in res["violations"].items()},
        "sharpe": float(res["sharpe"]),
        "annual_return": float(portfolio_return(w, MEAN)),
        "max_drawdown": BACKTEST_MAX_DD,
        "holdings": holdings,
        "equity": EQUITY,
    }
