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


HISTORICAL_WINDOWS={
    "global_financial_crisis":{"start":"2008-09-15","end":"2009-03-09"},
    "covid_crash":{"start":"2020-02-19","end":"2020-03-23"},
    "2022_rate_shock":{"start":"2022-01-03","end":"2022-10-12"},
    "crypto_2022_deleveraging":{"start":"2022-05-01","end":"2022-11-21"},
}

def historical_window_stress(factor_returns: pd.DataFrame, exposures: dict, windows=None):
    """Apply realized cumulative factor moves from named historical windows to current exposures."""
    windows=windows or HISTORICAL_WINDOWS
    rows=[]
    x=factor_returns.copy()
    x.index=pd.to_datetime(x.index)
    for name,w in windows.items():
        block=x.loc[w["start"]:w["end"]]
        if block.empty:
            rows.append({"scenario":name,"start":w["start"],"end":w["end"],"portfolio_return":float("nan"),"available":False})
            continue
        shocks=(1+block).prod()-1
        pnl=sum(exposures.get(k,0.0)*float(v) for k,v in shocks.items())
        rows.append({"scenario":name,"start":w["start"],"end":w["end"],"portfolio_return":pnl,"available":True,
                     **{f"shock_{k}":float(v) for k,v in shocks.items()}})
    return pd.DataFrame(rows)
