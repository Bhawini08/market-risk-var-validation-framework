from __future__ import annotations
import numpy as np
from scipy.stats import norm

def historical_var_es(returns, confidence=0.99):
    r=np.asarray(returns,float); alpha=1-confidence
    q=np.quantile(r,alpha); tail=r[r<=q]
    return {"var":float(-q),"es":float(-tail.mean()) if len(tail) else float(-q)}

def parametric_var_es(returns, confidence=0.99):
    r=np.asarray(returns,float); mu=r.mean(); sigma=r.std(ddof=1); alpha=1-confidence
    z=norm.ppf(alpha); q=mu+sigma*z
    es=-(mu-sigma*norm.pdf(z)/alpha)
    return {"var":float(-q),"es":float(es)}

def monte_carlo_var_es(returns, confidence=0.99, paths=200000, seed=42):
    r=np.asarray(returns,float); rng=np.random.default_rng(seed)
    sims=rng.normal(r.mean(),r.std(ddof=1),int(paths))
    return historical_var_es(sims,confidence)

def rolling_var(returns, window=250, confidence=0.99, method="historical"):
    import pandas as pd
    s=pd.Series(returns).dropna(); vals=[]
    for i in range(window,len(s)):
        sample=s.iloc[i-window:i]
        if method=="historical": x=historical_var_es(sample,confidence)
        elif method=="parametric": x=parametric_var_es(sample,confidence)
        else: x=monte_carlo_var_es(sample,confidence,paths=20000,seed=i)
        vals.append({"date":s.index[i],"realized_return":s.iloc[i],"var":x["var"],"es":x["es"]})
    return pd.DataFrame(vals).set_index("date")
