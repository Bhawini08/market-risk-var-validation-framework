import numpy as np
from risk.data import synthetic_portfolio_returns
from risk.var import historical_var_es,parametric_var_es,rolling_var
from risk.backtesting import exceedances,kupiec_pof,christoffersen_independence,conditional_coverage
from risk.volatility import ewma_volatility,fit_garch11
from risk.stress import stress_portfolio

def test_var_es_ordering():
    r=synthetic_portfolio_returns(800)
    for fn in [historical_var_es,parametric_var_es]:
        x95=fn(r,.95); x99=fn(r,.99)
        assert x99["var"]>=x95["var"]
        assert x99["es"]>=x99["var"]

def test_backtests_return_valid_probabilities():
    r=synthetic_portfolio_returns(900); roll=rolling_var(r,250,.99)
    e=exceedances(roll.realized_return,roll["var"])
    for x in [kupiec_pof(e,.01),christoffersen_independence(e),conditional_coverage(e,.01)]:
        assert 0<=x["p_value"]<=1

def test_volatility_and_stress():
    r=synthetic_portfolio_returns(700); ew=ewma_volatility(r); g=fit_garch11(r)
    assert (ew>0).all() and (g["volatility"]>0).all()
    s=stress_portfolio({"equity":1.0,"rates":0.0,"volatility":0.0,"liquidity":0.0})
    assert len(s)>=5
