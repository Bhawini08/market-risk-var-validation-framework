import argparse
import json
from pathlib import Path
import pandas as pd
from risk.data import synthetic_portfolio_returns, live_portfolio_returns
from risk.var import historical_var_es,parametric_var_es,monte_carlo_var_es,rolling_var
from risk.volatility import rolling_volatility,ewma_volatility,fit_garch11
from risk.backtesting import exceedances,kupiec_pof,christoffersen_independence,conditional_coverage
from risk.stress import stress_portfolio
parser=argparse.ArgumentParser(); parser.add_argument("--mode",choices=["synthetic","live"],default="synthetic"); args=parser.parse_args()
out=Path("results"); out.mkdir(exist_ok=True)
r=synthetic_portfolio_returns() if args.mode=="synthetic" else live_portfolio_returns(); rows=[]
for level in [.95,.99]:
    for name,fn in [("historical",historical_var_es),("parametric",parametric_var_es),("monte_carlo",monte_carlo_var_es)]:
        x=fn(r,level); rows.append({"method":name,"confidence":level,**x})
pd.DataFrame(rows).to_csv(out/"var_es_summary.csv",index=False)
roll=rolling_var(r,250,.99,"historical"); roll.to_csv(out/"rolling_var_backtest.csv")
exc=exceedances(roll.realized_return,roll["var"])
tests={"kupiec":kupiec_pof(exc,.01),"christoffersen":christoffersen_independence(exc),"conditional_coverage":conditional_coverage(exc,.01)}
(out/"backtest_tests.json").write_text(json.dumps(tests,indent=2))
v=pd.DataFrame({"rolling_20d":rolling_volatility(r,20),"ewma":ewma_volatility(r)}); g=fit_garch11(r); v["garch11"]=g["volatility"]; v.to_csv(out/"volatility_models.csv")
stress_portfolio({"equity":0.75,"rates":-2.5,"volatility":0.05,"liquidity":0.20,"crypto":0.05}).to_csv(out/"stress_tests.csv",index=False)
print(json.dumps(tests,indent=2))
