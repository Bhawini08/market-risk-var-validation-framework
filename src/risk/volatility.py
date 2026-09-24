import numpy as np
import pandas as pd
from scipy.optimize import minimize

def rolling_volatility(r,window=20,annualization=252):
    return pd.Series(r).rolling(window).std()*np.sqrt(annualization)

def ewma_volatility(r,lam=0.94,annualization=252):
    s=pd.Series(r).dropna(); var=np.empty(len(s)); var[0]=s.var()
    for i in range(1,len(s)): var[i]=lam*var[i-1]+(1-lam)*s.iloc[i-1]**2
    return pd.Series(np.sqrt(var*annualization),index=s.index,name="ewma_vol")

def fit_garch11(r,annualization=252):
    s=pd.Series(r).dropna(); x=s.to_numpy(float); scale=100.0; y=x*scale; init_var=np.var(y)
    def nll(theta):
        omega,alpha,beta=theta
        if omega<=0 or alpha<0 or beta<0 or alpha+beta>=0.999: return 1e12
        h=np.empty(len(y)); h[0]=init_var
        for t in range(1,len(y)): h[t]=omega+alpha*y[t-1]**2+beta*h[t-1]
        return .5*np.sum(np.log(2*np.pi)+np.log(h)+y*y/h)
    res=minimize(nll,[.02,.08,.90],method="Nelder-Mead",options={"maxiter":5000})
    if not res.success: raise RuntimeError("GARCH fit failed")
    omega,alpha,beta=res.x; h=np.empty(len(y)); h[0]=init_var
    for t in range(1,len(y)): h[t]=omega+alpha*y[t-1]**2+beta*h[t-1]
    vol=np.sqrt(h)/scale*np.sqrt(annualization)
    return {"omega":omega/scale**2,"alpha":alpha,"beta":beta,
            "volatility":pd.Series(vol,index=s.index,name="garch_vol")}
