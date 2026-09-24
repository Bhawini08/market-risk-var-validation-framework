import numpy as np
import pandas as pd

def synthetic_portfolio_returns(n=1800,seed=21):
    rng=np.random.default_rng(seed); idx=pd.bdate_range("2019-01-02",periods=n)
    z=rng.standard_t(df=7,size=n)*0.009
    vol=np.ones(n)
    for i in range(1,n): vol[i]=0.96*vol[i-1]+0.04*(1+4*abs(z[i-1]))
    r=0.00025+z*vol
    r[350:365]-=0.025; r[900:910]-=0.035; r[1300:1310]-=0.018
    return pd.Series(r,index=idx,name="portfolio_return")


def live_portfolio_returns(tickers=None,weights=None,start="2015-01-01",end=None):
    """Build a simple live validation portfolio from adjusted ETF returns."""
    import yfinance as yf
    tickers=tickers or ["SPY","QQQ","IWM","TLT","GLD"]
    raw=yf.download(tickers,start=start,end=end,auto_adjust=True,progress=False,threads=False)
    if raw.empty: raise RuntimeError("Yahoo Finance returned no data")
    if isinstance(raw.columns,pd.MultiIndex):
        px=raw["Close"] if "Close" in raw.columns.get_level_values(0) else raw.xs("Close",axis=1,level=1)
    else:
        px=raw[["Close"]].copy(); px.columns=[tickers[0]]
    px.columns=[str(c).upper() for c in px.columns]
    ret=px.pct_change(fill_method=None).dropna(how="any")
    if weights is None:
        w=np.repeat(1/len(ret.columns),len(ret.columns))
    else:
        w=np.asarray(weights,float); w=w/w.sum()
    return pd.Series(ret.to_numpy()@w,index=ret.index,name="portfolio_return")
