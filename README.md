# SwarmFolio: Mean-Variance vs Particle Swarm Portfolio Optimization

Comparing classical convex portfolio optimization (Markowitz mean-variance) against
a hand-rolled Particle Swarm Optimization (PSO) approach for portfolios with
real-world constraints (cardinality limits, min position sizes) that break
convexity.

## Status
🚧 Under construction — Week 1: data pipeline + exploration

## Structure
- `data/` — cached price data (gitignored, regenerate via scripts)
- `notebooks/` — exploration notebooks (Week 1-2 work happens here)
- `src/` — core modules (data loading, optimizers, backtest engine)
- `tests/` — pytest tests
- `dashboard/` — Streamlit app

## Setup
```
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Roadmap
- [ ] Week 1: Data pipeline, returns, covariance, exploratory plots
- [ ] Week 2: Mean-variance baseline, efficient frontier
- [ ] Week 3: Hand-rolled PSO optimizer with cardinality constraint
- [ ] Week 4: Walk-forward backtest, metrics, Streamlit dashboard, deploy
