import streamlit as st
import pandas as pd
from datetime import datetime
from data_collection import download_stock_data, clean_and_save_data, calculate_returns_and_risk
from problem_formulation import construct_qubo
from classical_solver import solve_qubo_classically
# from quantum_solver import solve_qubo as solve_qubo_quantum  # Uncomment if quantum works

st.set_page_config(page_title="Portfolio Optimizer", layout="wide")

st.title("🧠 Portfolio Optimizer")
st.markdown(
    "Easily find your **optimal stock portfolio** using modern optimization techniques."
)

# ----- SIDEBAR with advanced params -----
st.sidebar.header("Advanced Parameters")
lambda_val = st.sidebar.number_input(
    "λ (risk aversion)", min_value=0.0, max_value=100.0, value=1.0, step=0.1,
    help="How much you care about minimizing risk. Higher λ = safer."
)
gamma = st.sidebar.number_input(
    "γ (constraint penalty)", min_value=0.0, max_value=1000.0, value=10.0, step=1.0,
    help="Enforces that exactly K stocks are picked. Usually leave at 10."
)

# ----- MAIN INPUTS -----
with st.expander("How to Use (Click to Expand)", expanded=True):
    st.markdown("""
    **Instructions:**  
    1. Enter comma-separated stock tickers (e.g., `AAPL,MSFT,GOOGL`).  
    2. Choose your desired analysis period.  
    3. Set how many stocks to pick for your portfolio (`K`).  
    4. Click **Run Optimizer**!

    - λ (lambda): risk aversion.  
    - γ (gamma): how strictly to pick exactly K stocks.

    _Example: Tickers = `AAPL,MSFT,GOOGL,AMZN,JPM`, K = 2, λ = 1.0, γ = 10.0_
    """)

tickers = st.text_input(
    "Stock Tickers (comma-separated):", 
    "AAPL,MSFT,GOOGL,AMZN,JPM", 
    help="E.g., AAPL, MSFT, GOOGL, AMZN, JPM"
)

col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input(
        "Start Date", datetime(2020, 1, 1),
        help="Start of your backtest window"
    )
with col2:
    end_date = st.date_input(
        "End Date", datetime.now(),
        help="End of your backtest window"
    )
with col3:
    K = st.number_input(
        "Stocks to pick (K)", min_value=1, max_value=20, value=2,
        help="Number of stocks to select for your portfolio"
    )

# --- Solver choice ---
# solver_type = st.radio("Solver Type", ["Classical", "Quantum (beta, may not work)"])
solver_type = "Classical"  # Uncomment above if quantum available

st.divider()
run_button = st.button("🚀 Run Optimizer")

if run_button:
    try:
        tickers_list = [t.strip().upper() for t in tickers.split(',') if t.strip()]
        st.info(f"Fetching data for: {', '.join(tickers_list)}")
        stock_data = download_stock_data(tickers_list, str(start_date), str(end_date))
        clean_data = clean_and_save_data(stock_data, 'stock_data.csv')
        mu, Sigma = calculate_returns_and_risk(clean_data)
        st.success("Data downloaded & cleaned successfully!")

        # Show a preview
        with st.expander("Show price data table"):
            st.dataframe(clean_data.tail(10))

        # Construct QUBO
        Q = construct_qubo(mu, Sigma, K, lambda_val=lambda_val, gamma=gamma)

        # Solve
        if solver_type == "Classical":
            sol, val = solve_qubo_classically(Q)
        # elif solver_type == "Quantum (beta, may not work)":
        #     quantum_result = solve_qubo_quantum(Q, reps=1)
        #     sol = quantum_result.x
        #     val = quantum_result.fval

        selected = [tickers_list[i] for i in range(len(sol)) if sol[i] == 1]
        not_selected = [tickers_list[i] for i in range(len(sol)) if sol[i] == 0]
        st.subheader("📊 Optimization Results")
        st.markdown("**🟢 Recommended to INVEST (Buy/Keep):**")
        st.write(selected)
        st.markdown("**🔴 Not Selected (Consider Hold/Sell):**")
        st.write(not_selected)
        st.markdown(f"**Bitstring (solution):** `{sol}`")
        st.markdown(f"**Objective value:** `{val}`")

        # --- Show mean returns and risk for all stocks ---
        st.markdown("### 📈 Stock Mean Returns & Risk")
        stats_df = pd.DataFrame({
            "Expected Return": mu,
            "Risk (Variance)": Sigma.values.diagonal()
        })
        st.dataframe(stats_df)
        st.bar_chart(stats_df["Expected Return"])

        # --- Show scatterplot Risk vs Return ---
        st.markdown("#### Risk vs Return (selected in green):")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.scatter(stats_df["Risk (Variance)"], stats_df["Expected Return"], c=['g' if s in selected else 'r' for s in tickers_list])
        for i, t in enumerate(tickers_list):
            ax.annotate(t, (stats_df["Risk (Variance)"][i], stats_df["Expected Return"][i]))
        ax.set_xlabel("Risk (Annualized Variance)")
        ax.set_ylabel("Expected Return")
        st.pyplot(fig)

        st.success("Done! Adjust parameters and re-run for different results.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")

# ---- Footer: Add parameter summary
with st.expander("What do the parameters mean?"):
    st.markdown("""
- **K (Stocks to pick):** Number of stocks the optimizer will choose for your portfolio.
- **lambda (λ):** How much to avoid risk (higher = less risk).
- **gamma (γ):** How strictly to enforce the “pick K” rule.

_This app fetches real data, runs portfolio optimization, and gives you a simple, transparent recommendation._  
    """)
