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

## Stress testing

Historical-style shock scenarios and hypothetical shocks covering equities, rates, volatility, correlation, liquidity, and optional digital-asset shocks.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest -q
python scripts/run_risk_analysis.py
streamlit run dashboard/app.py
```

Synthetic mode is used for reproducible engineering validation. Live market data and historical crisis-window verification are reserved for the final validation pass.
