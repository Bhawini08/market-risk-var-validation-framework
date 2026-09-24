# Methodology

## VaR and Expected Shortfall

The framework compares historical, Gaussian parametric, and Monte Carlo VaR/Expected Shortfall at 95% and 99%.

Expected Shortfall is reported alongside VaR because VaR identifies a quantile threshold but does not describe the severity of losses once that threshold is crossed.

## Volatility models

Volatility diagnostics compare:

- rolling historical volatility
- RiskMetrics-style EWMA
- Gaussian GARCH(1,1)

These models respond differently to changing market conditions, making them useful for diagnosing volatility persistence and regime shifts.

## VaR backtesting

Validation is formal rather than visual only.

### Kupiec proportion-of-failures test

Kupiec tests whether the observed exceedance frequency is consistent with the model's nominal confidence level.

In the current live run, the p-value is about **0.345**, so unconditional coverage alone is not rejected.

### Christoffersen independence test

Christoffersen tests whether exceedances arrive independently through time.

The current live run produces a p-value of about **0.0004**, strongly rejecting independence. The breach sequence contains more clustering than a correctly specified independent-hit model would imply.

### Conditional coverage

Conditional coverage combines exceedance frequency and independence.

The current p-value is about **0.0013**, so the full VaR specification is rejected despite an acceptable unconditional breach count.

This is an important distinction: a VaR model can appear calibrated on average while still failing during volatility clusters.

## Stress testing

Stress testing is separate from VaR. VaR is a probabilistic model based on recent or modeled return distributions, while stress tests ask how the portfolio behaves under explicitly chosen adverse scenarios.

The framework includes historical-style crisis windows and hypothetical shocks to major market factors.

## Interpretation

The live results suggest that static or slowly adapting VaR specifications can match the average exceedance rate while understating serial dependence in losses.

That is a model-validation finding, not a software failure. The purpose of the framework is to surface precisely this type of misspecification.
