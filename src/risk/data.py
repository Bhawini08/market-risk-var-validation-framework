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
