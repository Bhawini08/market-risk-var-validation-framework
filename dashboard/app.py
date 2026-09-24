import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Market Risk Framework",layout="wide")
st.title("Market Risk, VaR & Model Validation Framework")
p=Path("results/var_es_summary.csv")
if not p.exists():
    st.info("Run scripts/run_risk_analysis.py first.")
else:
    st.subheader("VaR / Expected Shortfall")
    st.dataframe(pd.read_csv(p),use_container_width=True)
    v=Path("results/volatility_models.csv")
    if v.exists():
        st.subheader("Volatility models")
        st.line_chart(pd.read_csv(v,index_col=0).tail(500))
    b=Path("results/rolling_var_backtest.csv")
    if b.exists():
        st.subheader("Rolling 99% VaR backtest")
        st.line_chart(pd.read_csv(b,index_col=0)[["var"]].tail(500))
    s=Path("results/stress_tests.csv")
    if s.exists():
        st.subheader("Stress tests")
        st.dataframe(pd.read_csv(s),use_container_width=True)
