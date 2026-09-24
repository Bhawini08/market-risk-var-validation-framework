# Methodology

The framework compares historical, Gaussian parametric, and Monte Carlo VaR/Expected Shortfall at 95% and 99%. Expected Shortfall is reported alongside VaR because tail severity matters after the quantile is breached.

Volatility diagnostics compare rolling realized volatility, RiskMetrics-style EWMA, and a Gaussian GARCH(1,1) maximum-likelihood fit.

VaR validation is formal rather than visual only. Kupiec tests unconditional exceedance frequency, Christoffersen tests exceedance independence, and conditional coverage combines both dimensions. A model can therefore fail because it produces too many or too few breaches, or because breaches cluster.

Stress testing is separate from VaR. Scenarios map factor shocks into portfolio P&L through explicit exposures. Synthetic scenarios validate the software only; historical crisis scenarios should be re-estimated from verified market windows during live-data testing.
