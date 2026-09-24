import numpy as np
from scipy.stats import chi2

def exceedances(realized_returns,var_series):
    r=np.asarray(realized_returns,float); v=np.asarray(var_series,float)
    return (r < -v).astype(int)

def kupiec_pof(exceed,alpha):
    x=np.asarray(exceed,int); n=len(x); failures=x.sum()
    if n==0: return {"lr":np.nan,"p_value":np.nan,"failures":0,"n":0}
    pi=np.clip(failures/n,1e-12,1-1e-12); a=np.clip(alpha,1e-12,1-1e-12)
    ll0=(n-failures)*np.log(1-a)+failures*np.log(a)
    ll1=(n-failures)*np.log(1-pi)+failures*np.log(pi)
    lr=-2*(ll0-ll1)
    return {"lr":float(lr),"p_value":float(1-chi2.cdf(lr,1)),"failures":int(failures),"n":n}

def christoffersen_independence(exceed):
    x=np.asarray(exceed,int)
    if len(x)<2: return {"lr":np.nan,"p_value":np.nan}
    n00=n01=n10=n11=0
    for a,b in zip(x[:-1],x[1:]):
        if a==0 and b==0:n00+=1
        elif a==0 and b==1:n01+=1
        elif a==1 and b==0:n10+=1
        else:n11+=1
    p01=n01/max(n00+n01,1); p11=n11/max(n10+n11,1); p=(n01+n11)/max(n00+n01+n10+n11,1)
    eps=1e-12
    def term(n,pv): return n*np.log(np.clip(pv,eps,1-eps))
    ll0=term(n00+n10,1-p)+term(n01+n11,p)
    ll1=term(n00,1-p01)+term(n01,p01)+term(n10,1-p11)+term(n11,p11)
    lr=-2*(ll0-ll1)
    return {"lr":float(lr),"p_value":float(1-chi2.cdf(lr,1)),"n00":n00,"n01":n01,"n10":n10,"n11":n11}

def conditional_coverage(exceed,alpha):
    k=kupiec_pof(exceed,alpha); c=christoffersen_independence(exceed)
    lr=k["lr"]+c["lr"]
    return {"lr":float(lr),"p_value":float(1-chi2.cdf(lr,2))}
