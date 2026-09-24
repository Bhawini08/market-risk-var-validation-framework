# Market Risk, VaR & Model Validation Framework

A quantitative market-risk platform for estimating Value at Risk and Expected Shortfall, comparing volatility models, formally backtesting VaR forecasts, and running historical and hypothetical stress scenarios.

## Risk models

- Historical VaR / ES
- Parametric Gaussian VaR / ES
- Monte Carlo VaR / ES
- 95% and 99% confidence levels

## Volatility

- Rolling historical volatility
- EWMA
- GARCH(1,1)

## Validation

- Exceedance analysis
- Kupiec proportion-of-failures test
- Christoffersen independence test
- Conditional coverage test

## Live backtest snapshot

For the live VaR backtest:

- Observations: **2,698**
- VaR exceedances: **32**
- Kupiec POF p-value: **0.345**
- Christoffersen independence p-value: **0.0004**
- Conditional coverage p-value: **0.0013**

Interpretation:

- The Kupiec result does **not** reject the model on unconditional exceedance frequency alone.
- The Christoffersen test strongly rejects independence, indicating exceedances cluster in time.
- The combined conditional-coverage test also rejects the model.

So the model gets the long-run breach count roughly right, but misses time-varying tail risk during stressed periods. That is exactly why formal validation needs both frequency and independence tests.

## Stress testing

Historical-style and hypothetical scenarios cover equities, rates, volatility, correlation, liquidity, and optional digital-asset shocks.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest -q
python scripts/run_risk_analysis.py --mode live
streamlit run dashboard/app.py
```

## Research discipline

VaR is treated as a model to validate, not a number to trust automatically. Expected Shortfall, volatility-model comparison, breach frequency, breach clustering, and stress tests are reported together so model weaknesses remain visible.
