import pandas as pd

DEFAULT_SCENARIOS={
"equity_crash":{"equity":-0.20,"rates":0.00,"volatility":1.0,"liquidity":0.0},
"rates_up_200bp":{"equity":-0.05,"rates":0.02,"volatility":0.30,"liquidity":0.0},
"volatility_doubles":{"equity":-0.08,"rates":0.00,"volatility":1.0,"liquidity":0.0},
"correlation_convergence":{"equity":-0.12,"rates":0.01,"volatility":0.70,"liquidity":0.0},
"liquidity_shock":{"equity":-0.10,"rates":0.005,"volatility":0.50,"liquidity":-0.03},
"crypto_shock":{"equity":-0.03,"rates":0.0,"volatility":0.25,"liquidity":-0.01,"crypto":-0.40},
}

def stress_portfolio(exposures: dict, scenarios=None):
    scenarios=scenarios or DEFAULT_SCENARIOS
    rows=[]
    for name,shocks in scenarios.items():
        pnl=sum(exposures.get(k,0.0)*v for k,v in shocks.items())
        rows.append({"scenario":name,"portfolio_return":pnl,**shocks})
    return pd.DataFrame(rows)
