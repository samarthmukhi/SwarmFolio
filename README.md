# SwarmFolio

**Particle swarm optimization for constrained portfolios — and an honest answer when none exists.**

🔗 **Live demo:** [swarmfolio.vercel.app](https://swarmfolio.vercel.app)
*(Backend is on a free tier and sleeps when idle — the first request may take ~30–60s to wake.)*

SwarmFolio pits classical **Markowitz mean-variance optimization** against a **hand-written Particle Swarm Optimization (PSO)** algorithm, specifically for portfolios with the real-world constraints that break the convex math the classical method relies on.

---

## The problem

Standard mean-variance optimization is *convex* — a quadratic solver finds the single best portfolio instantly. But add the constraints real investors actually face:

- **Cardinality:** *"hold at most K of N assets"*
- **Minimum position size:** *"no positions smaller than X%"*
- **Minimum holdings:** *"hold at least K names"* (diversification)

…and the problem becomes **non-convex / combinatorial**. There's no longer a clean closed-form answer, and the convex solver either can't express the constraint or breaks on it. This is exactly where a metaheuristic like PSO earns its place.

## Why PSO

I first used PSO for **path planning on an autonomous marine-cleanup robot** (NautiClean — INSPIRE–MANAK National Award, Govt. of India; first-author paper, IJERSTE Vol. 14(10), 2025). SwarmFolio applies the *same class of algorithm* to a completely different domain — portfolio allocation — because constrained allocation is non-convex, and that's precisely where swarm search beats a convex solver. **Same technique, different problem.**

## Method

```
prices → returns → covariance     (data layer)
        │
        ├── Markowitz max-Sharpe   (convex baseline)
        └── PSO                    (hand-written swarm)
                  ├── constraints via penalty method  → beats Markowitz on the non-convex case
                  ├── feasibility layer                → reports when no allocation can satisfy the rules
                  └── walk-forward backtest            → out-of-sample, look-ahead-safe
```

- **PSO core** (`src/pso.py`): particles = candidate weight vectors; velocity = inertia + pull-to-personal-best + pull-to-global-best; fitness = Sharpe ratio; long-only + fully-invested enforced by a repair step.
- **Constraints:** a penalty method — the fitness is Sharpe *minus* a penalty for every violation, so the swarm learns to avoid rule-breaking allocations.
- **Feasibility layer:** runs the swarm, then checks whether even its best result obeys every constraint. If not, it honestly reports **infeasible** with the exact violations — instead of returning a fake best-effort.
- **Backtest** (`src/backtest.py`): walk-forward, trains only on strictly-past data at each rebalance, models transaction costs.

## Results

- **Correctness:** on the unconstrained (convex) case, the hand-written PSO converges to the *same* portfolio as the analytic Markowitz solver — **Sharpe 1.377 vs 1.380** (within 0.2%).
- **Necessity:** with `max 8 holdings, min 5%` constraints, PSO returns a **fully feasible** portfolio (0 violations) — a problem the convex solver can't express. The trade-off is a measurable Sharpe cost, i.e., the honest price of a runnable portfolio.
- **Honesty:** on impossible constraints (e.g. *5 holdings, each ≥ 30% = 150% of capital*), the feasibility layer correctly reports **infeasible** with the exact shortfall.
- **Backtest:** a walk-forward backtest reproduces the well-known **"1/N puzzle"** — naive equal-weight (Sharpe ≈ 0.99) *beats* out-of-sample max-Sharpe optimization (≈ 0.85), both beating the market (SPY ≈ 0.66). Optimization looks great in-sample and overfits out-of-sample.

## Honest limitations

- **Backtests are necessary, not sufficient.** Past performance ≠ future results. Results are evidence, not proof.
- **In-sample ≠ out-of-sample.** Unconstrained max-Sharpe overfits the estimation window (see the 1/N result above). PSO's value here is constraint-handling, not beating 1/N on raw Sharpe.
- **Survivorship bias:** the universe uses tickers that still exist today.
- **Single data source** (yfinance), and a simple linear transaction-cost model.
- **PSO is stochastic** — it's a heuristic search, so results vary slightly between runs, and "infeasible" means *no feasible solution found*, not a mathematical proof of impossibility.
- **Not investment advice.** This is a research/portfolio project.

## Tech

Python · NumPy · SciPy · pandas · yfinance · FastAPI (API) · React + Vite + Tailwind + Framer Motion + Recharts (frontend) · deployed on Vercel + Render.

## Run locally

```bash
# backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --port 8000

# frontend (in another terminal)
cd frontend
npm install
npm run dev        # http://localhost:5173
```

## Status

🟢 **Shipped and live.** Data layer, Markowitz baseline, hand-written PSO, constraints, feasibility layer, walk-forward backtest, and a deployed React + FastAPI app are all complete.
