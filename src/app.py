import streamlit as st
import pandas as pd
from datetime import datetime
from data_collection import download_stock_data, clean_and_save_data, calculate_returns_and_risk
from problem_formulation import construct_qubo
from classical_solver import solve_qubo_classically

st.title("Portfolio Optimizer (Classical Version)")

# --------------- EXPLANATIONS ---------------
st.markdown("""
**Instructions:**
- Enter the list of stock tickers you want to analyze (example: `AAPL, MSFT, GOOGL, AMZN, JPM`)
- Choose the start and end dates for your backtest period.
- Select how many stocks you want the optimizer to pick (`K`).
- Adjust the parameters `lambda` and `gamma` to change risk and constraint weightings (see tooltips).
""")

# ---- Input fields with tooltips and examples ----

tickers = st.text_input(
    "Enter stock tickers (comma-separated)",
    "AAPL,MSFT,GOOGL,AMZN,JPM",
    help="Example: AAPL, MSFT, GOOGL, AMZN, JPM (U.S. stock tickers, comma-separated, no spaces needed)."
)

start_date = st.date_input(
    "Start date",
    datetime(2020, 1, 1),
    help="The first day of your analysis window. Example: 2020-01-01"
)

end_date = st.date_input(
    "End date",
    datetime.now(),
    help="The last day of your analysis window. Example: 2025-07-29"
)

K = st.number_input(
    "Stocks to pick (K)",
    min_value=1, max_value=10, value=2,
    help="How many stocks should be included in the optimal portfolio? Example: 2"
)

lambda_val = st.number_input(
    "lambda (risk aversion)",
    min_value=0.0, max_value=100.0, value=1.0, step=0.1,
    help="Controls how much risk matters. Higher lambda = safer (less risky, more stable). Example: 1.0"
)

gamma = st.number_input(
    "gamma (constraint penalty)",
    min_value=0.0, max_value=1000.0, value=10.0, step=1.0,
    help="How hard the optimizer enforces picking exactly K stocks. Higher gamma = more strict. Example: 10.0"
)

# -------- RUN OPTIMIZER --------

if st.button("Run Optimizer"):
    tickers_list = [t.strip().upper() for t in tickers.split(',')]
    stock_data = download_stock_data(tickers_list, str(start_date), str(end_date))
    clean_data = clean_and_save_data(stock_data, 'stock_data.csv')
    mu, Sigma = calculate_returns_and_risk(clean_data)
    Q = construct_qubo(mu, Sigma, K, lambda_val=lambda_val, gamma=gamma)
    sol, val = solve_qubo_classically(Q)
    selected = [tickers_list[i] for i in range(len(sol)) if sol[i] == 1]
    st.markdown("### 🟢 **Selected Stocks:**")
    st.write(selected)
    st.markdown("#### 🧬 Best bitstring (solution):")
    st.write(sol)
    st.markdown(f"#### 💡 Objective value: `{val}`")

# ---- OPTIONAL: ADD MORE HELPFUL EXPLANATIONS BELOW ----
st.markdown("""
---
**Parameter Explanations:**
- **tickers:** These are the stock symbols, like `AAPL` for Apple, `MSFT` for Microsoft.
- **K (Stocks to pick):** How many stocks you want to select for your final portfolio. For example, if you set this to 2, the optimizer will try to pick the best 2 stocks.
- **lambda (risk aversion):** Controls how much you care about minimizing risk. Set higher to avoid volatile stocks. Set lower if you want to risk more for higher potential return.
- **gamma (constraint penalty):** Makes the optimizer enforce your “pick K stocks” rule. You can usually leave this at 10.0 unless you know what you’re doing.

**Example run:**  
- Tickers: `AAPL, MSFT, GOOGL, AMZN, JPM`  
- Start date: `2020-01-01`  
- End date: `2025-07-29`  
- K: `2`  
- lambda: `1.0`  
- gamma: `10.0`
""")
